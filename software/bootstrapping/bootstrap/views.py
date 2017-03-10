from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

# location stuff
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

from . import models, serializers, functions, os

from datetime import datetime, date, timedelta, timezone
import json, requests, uuid, socket

@login_required
def log(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'log.log')
    # print(path)
    with open(path, 'r') as myfile:
        data=myfile.read()
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
        json_data = json.loads(request.body.decode("utf-8"))
        json_ret = {}
        print("DEBUG: ", json_data)

        ip_address = json_data["ip_address"]

        try:
            socket.inet_aton(ip_address)  # verify if IP address valid
            ip = get_real_ip(request)
            if ip is not None:
                if ip_address is not ip:
                    json_ret["status"] = "fail"
                    json_ret["reason"] = "IP mismatch, using retrieved IP instead of submitted."
                    ip_address = ip
            else:
                json_ret["status"] = "fail"
                json_ret["reason"] = "IP not found, using user submitted IP."
        except socket.error:
            json_ret["status"] = "fail"
            json_ret["reason"] = "IP not valid."

        if 'port' not in json_data:
            port = 8000  # default assume port is 8000
        else:
            port = json_data["port"]

        try:
            int(port)
        except ValueError:
            json_ret["status"] = "fail"
            json_ret["reason"] = "Port not valid."

        # needs rethinking about if a peer decides to connect through VPN
        if 'location_lat' not in json_data and 'location_long' not in json_data:
            g = GeoIP2()
            (location_lat, location_long) = g.lat_lon(ip_address)
            json_ret["location_lat"] = location_lat
            json_ret["location_long"] = location_long
            json_ret["location_method"] = "geolocation"
        else:
            location_lat = json_data["location_lat"]
            location_long = json_data["location_long"]
            json_ret["location_method"] = "explicit"

        geolocator = GoogleV3()
        location = geolocator.reverse(query=str(location_lat) + ", " + str(location_long), exactly_one=True)

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

        ret = models.peer.objects.create(
            ip_address=ip_address,
            port=port,
            location_lat=location_lat,
            location_long=location_long,
            location_city=location_city,
            location_country=location_country,
            # timestamp is automatic
            token_update=token_update,
            token_peer=token_peer,
            active=True,
        )

        if ret is not None:
            json_ret["status"] = "success"
            return Response(json_ret, status=status.HTTP_201_CREATED)
        else:
            json_ret["status"] = "fail"
            return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)


class update(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        '''
        Used to update the peer entry.
        :param request:
        :return:
        '''
        if 'ip_address' in request.POST and 'port' in request.POST:
            ip_address = request.POST["ip_address"]
            port = request.POST["port"]
        token = request.META['HTTP_AUTHORIZATION']

        (peer_obj, ret) = functions.get_peer_entry(ip_address, port, token)
        if peer_obj is not None:
            # TODO
            pass
        return ret


class deregister(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        '''
        Used to remove the peer entry from the database. POST, not GET, same as logging out.
        :param request:
        :return:
        '''
        if 'ip_address' in request.POST and 'port' in request.POST:
            ip_address = request.POST["ip_address"]
            port = request.POST["port"]
        token = request.META['HTTP_AUTHORIZATION']

        (peer_obj, ret) = functions.get_peer_entry(ip_address, port, token)
        if peer_obj is not None:
            peer_obj.delete()
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
        if 'ip_address' in request.POST and 'port' in request.POST:
            ip_address = request.POST["ip_address"]
            port = request.POST["port"]
        token = request.META['HTTP_AUTHORIZATION']

        (peer_obj, ret) = functions.get_peer_entry(ip_address, port, token)
        if peer_obj is not None:
            peer_obj.active = True
            peer_obj.save()
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

        if country is not None:
            data = data.filter(location_country=country)
        if city is not None:
            data = data.filter(location_city=city)
        if distance is not None:
            pass

        serializer = serializers.get_peers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
