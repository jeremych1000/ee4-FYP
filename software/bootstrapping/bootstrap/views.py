from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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

from . import models, serializers

from datetime import datetime, date, timedelta, timezone
import json, requests, uuid


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

        ip = get_real_ip(request)
        if ip is not None:
            if ip_address != ip:
                json_ret["ip_address"] = "IP mismatch, using retrieved IP instead of submitted."
                ip_address = ip
        else:
            json_ret["ip_address"] = "IP not found, using user submitted IP."


        if 'port' not in json_data:
            port = 8000  # default assume port is 8000
        else:
            port = json_data["port"]

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
    pass

class deregister(APIView):
    pass

class keep_alive(APIView):
    pass

class get_peers(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, distance=None, city=None, country=None):
        '''
        Gets a list of peers from the bootstrapping server.
        TODO: Implement parameters to filter the GET request by distance, country, etc?
        :param request:
        :return:
        '''
        data = models.peer.objects.all()

        if country is not None:
            data = data.filter(location_country=country)
        if city is not None:
            data = data.filter(location_city=city)
        if distance is not None:
            pass

        serializer = serializers.peer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

