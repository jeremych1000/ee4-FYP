from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.db import *
from django.db.utils import *
from django.core.exceptions import *

# location stuff
import geoip2
from django.contrib.gis.geoip2 import GeoIP2
from geopy.geocoders import GoogleV3

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from ipware.ip import get_real_ip

from bootstrap import models, serializers, functions
from bootstrap.encrypt import encrypt, decrypt

import datetime, json, requests, uuid, socket, os


@login_required
def log(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'log.log')
    # print(path)
    with open(path, 'r') as myfile:
        data = myfile.read()
    return HttpResponse(data, content_type='text/plain')


class register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        '''
        Accepts JSON POST data containing information about the peer and adds it into the bootstrapping database.
        First queries the incoming IP:port using GET to see if it is an actual peer. (TODO: some algo to check)
        :param request: Django HTTP request
        :return: HTTP 200 if successful
        '''
        json_data = json.loads(decrypt(request.body, settings.FERNET_KEY))
        print("json data is _____", json_data, type(json_data))
        json_ret = {}
        json_ret_fail = {}  # use this dictionary for return fail

        print("DEBUG: ", json_data)

        ip_address = json_data["ip_address"]

        try:
            socket.inet_aton(ip_address)  # verify if IP address valid
            ip = get_real_ip(request)
            if ip is not None:
                if ip_address != ip:
                    json_ret_fail["status"] = "fail"
                    json_ret_fail[
                        "reason"] = "IP mismatch, using retrieved IP (" + ip + ") instead of submitted (" + ip_address + ")."
                    ip_address = ip
            else:
                json_ret_fail["status"] = "fail"
                json_ret_fail["reason"] = "IP not found, using user submitted IP."
        except socket.error:
            json_ret_fail["status"] = "fail"
            json_ret_fail["reason"] = "IP not valid."

        if 'port' not in json_data:
            port = 8000  # default assume port is 8000
        else:
            port = json_data["port"]

        try:
            int(port)
        except ValueError:
            json_ret_fail["status"] = "fail"
            json_ret_fail["reason"] = "Port not valid."

        # needs rethinking about if a peer decides to connect through VPN
        if 'location_lat' not in json_data and 'location_long' not in json_data:
            g = GeoIP2()
            address_type = "External"

            try:
                (location_lat, location_long) = g.lat_lon(ip_address)
            except geoip2.errors.AddressNotFoundError:
                location_lat = 0
                location_long = 0
                address_type = "Internal"
            if location_lat is not None or location_long is not None:
                json_ret["location_lat"] = location_lat
                json_ret["location_long"] = location_long
                json_ret["location_method"] = "geolocation"
        else:
            location_lat = json_data["location_lat"]
            location_long = json_data["location_long"]
            json_ret["location_method"] = "explicit"

        geolocator = GoogleV3()
        location = geolocator.reverse(query=str(location_lat) + ", " + str(location_long), exactly_one=True)

        location_city = "Empty"
        location_country = "Empty"
        if location is not None:
            for i in location.raw["address_components"]:
                if "country" in i["types"]:
                    location_country = i["long_name"]
                    json_ret["location_country"] = location_country
                elif "postal_town" in i["types"]:
                    location_city = i["long_name"]
                    json_ret["location_city"] = location_city

        token_update = uuid.uuid4()
        token_peer = uuid.uuid4()
        json_ret["token_update"] = token_update
        json_ret["token_peer"] = token_peer

        try:
            ret = models.peer.objects.create(
                ip_address=ip_address,
                port=port,
                type=address_type,
                location_lat=location_lat,
                location_long=location_long,
                location_city=location_city,
                location_country=location_country,
                # timestamp is automatic
                last_seen=timezone.now(),
                minutes_connected=0,
                token_update=token_update,
                token_peer=token_peer,
                active=True,
                requires_peer_broadcasting=True,
            )
        except IntegrityError:
            # either reregistering or fake
            # check previous token, if correct, change all tokens, broadcast to peers
            # deny if not
            json_ret_fail["status"] = "fail"
            json_ret_fail["reason"] = "Unique key failed"
            # expect peer will issue a PATCH request if conflict
            return HttpResponse(json_ret_fail, status=status.HTTP_409_CONFLICT)

        if ret is not None:
            json_ret["status"] = "success"
            return Response(json_ret, status=status.HTTP_201_CREATED)
        else:
            json_ret_fail["status"] = "fail"
            return Response(json_ret_fail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # re-registering
        # check token, if correct, change, broadcast, deny if not
        json_data = json.loads(decrypt(request.body, settings.FERNET_KEY))
        json_ret = {}

        try:
            peer_obj = models.peer.objects.get(
                ip_address=json_data["ip_address"],
                port=json_data["port"],
                token_update=json_data["token_update"],
                token_peer=json_data["token_peer"]
            )
        except ObjectDoesNotExist:
            json_ret["status"] = "failure"
            json_ret["reason"] = "Peer object not found"
            return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)

        new_token_update = uuid.uuid4()
        new_token_peer = uuid.uuid4()

        peer_obj.token_update = new_token_update
        peer_obj.token_peer = new_token_peer
        peer_obj.requires_peer_broadcasting = True
        try:
            peer_obj.save()
        except Exception as e:
            print("Exception occurred while saving updated peer entry - ", str(e))
            json_ret["status"] = "failure"
            json_ret["reason"] = str(e)
            return Response(json_ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        json_ret["status"] = "success"
        json_ret["reason"] = "Updated peer record, updating all other peers now."
        json_ret["token_update"] = str(new_token_update)
        json_ret["token_peer"] = str(new_token_peer)
        return Response(json_ret, status=status.HTTP_200_OK)

    def delete(self, request):
        json_data = json.loads(decrypt(request.body, settings.FERNET_KEY))

        ip_address = json_data["ip_address"]
        port = json_data["port"]

        try:
            peer_obj = models.peer.objects.get(ip_address=ip_address, port=port)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # else
        try:
            peer_obj.delete()
        except Exception as e:
            print("Exception while deleting peer - ", str(e))
        return Response(status=status.HTTP_200_OK)


class update(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        '''
        Used to update the peer entry.
        :param request:
        :return:
        '''
        json_data = json.loads(decrypt(request.body, settings.FERNET_KEY))

        if "ip_address" in json_data:
            ip_address = json_data["ip_address"]
        if "port" in json_data:
            port = json_data["port"]
        token = request.META['HTTP_AUTHORIZATION']

        (peer_obj, ret) = functions.get_peer_entry(ip_address, port, token)
        if peer_obj is not None:
            # TODO
            pass
        return ret


class keep_alive(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        '''
        Used to refresh database entry of peer to prevent bootstrapping server from marking as inactive.
        Only sets active, for updating data please use /update/.
        :param request:
        :return:
        '''
        json_data = json.loads(decrypt(request.body, settings.FERNET_KEY))

        if "ip_address" in json_data:
            ip_address = json_data["ip_address"]
        if "port" in json_data:
            port = json_data["port"]
        token = request.META['HTTP_AUTHORIZATION']
        print("recieved token is ", token)

        (peer_obj, ret) = functions.get_peer_entry(ip_address, port, token)
        if peer_obj is not None:
            peer_obj.last_seen = timezone.now()
            peer_obj.active = True
            peer_obj.save()

        print("keep alive ", ret.data)
        return ret


class get_peers(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, distance=None, city=None, country=None):
        # TODO: Implement parameters to filter the GET request by distance, country, etc?
        '''
        Gets a list of peers from the bootstrapping server.
        :param request:
        :return:
        '''
        json_ret = {}
        try:
            data = models.peer.objects.all()
        except models.peer.DoesNotExist:
            json_ret["status"] = "fail"
            json_ret["reason"] = "Combination not found, please register."
            return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)

        # dont send details of inactive peers?
        data = data.filter(active=True)

        if country is not None:
            data = data.filter(location_country=country)
        if city is not None:
            data = data.filter(location_city=city)
        if distance is not None:
            pass

        if len(data) != 0:
            serializer = serializers.get_peers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
