from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.db import *
from django.db.utils import *
from django.core.exceptions import *

import os, requests, json, datetime
from collections import OrderedDict
from ipware.ip import get_ip

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import models, serializers


class state(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # return 200 if have registered

        if len(models.bootstrap.objects.all()) > 0:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        # accept keep alive signals from other peers to update in peer_list model
        token = request.META['HTTP_AUTHORIZATION']
        json_data = json.loads(request.body.decode("utf-8"))
        json_ret = {}

        try:
            self_token = str(models.peer_list.objects.all().filter(is_self=True).first().token)
        except Exception as e:
            print("Exception occursed when finding self peer object - ", e)

        try:
            peer_obj = models.peer_list.objects.get(ip_address=json_data["ip_address"], port=json_data["port"])
        except ObjectDoesNotExist:
            json_ret["status"] = "failure"
            json_ret["reason"] = "No such peer in the database, please check IP and port."
            return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception occured when finding peer object - ", e, e.__cause__)

        if self_token == token:
            peer_obj.active = True
            try:
                peer_obj.save()
            except Exception as e:
                print("Exception occured when saving - ", e, e.__cause__)

            json_ret["status"] = "success"
            json_ret["reason"] = "Successfully updated peer record."
            return Response(json_ret, status=status.HTTP_200_OK)
        else:
            json_ret["status"] = "failure"
            json_ret["reason"] = "Token error"
            # return Response(json_ret, status=status.HTTP_401_UNAUTHORIZED)
            return Response(json_ret, status=status.HTTP_401_UNAUTHORIZED)


class peers(APIView):
    permission_classes = (AllowAny,)

    def patch(self, request):
        json_data = json.loads(request.body.decode("utf-8"))
        print("peers patch")
        print(json_data)

        for i in json_data["peers"]:
            print(i)
            try:
                peer = models.peer_list.objects.get(ip_address=i["ip_address"], port=i["port"])
            except ObjectDoesNotExist:
                print("No such peer found, adding now.")
                try:
                    ret = models.peer_list.objects.create(
                        ip_address=i["ip_address"],
                        port=i["port"],
                        is_self=False,
                        location_lat=i["location_lat"],
                        location_long=i["location_long"],
                        location_city=i["location_city"],
                        location_country=i["location_country"],
                        # time_accepted=
                        last_updated=i["last_seen"],
                        token=i["token_peer"],
                        active=True,
                        # no_plates=
                        # no_matching_plates=
                        # trust=
                    )
                except Exception as e:
                    print("Error while adding new peer to list form PATCH - ", str(e))

                if ret is not None:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                print("Attempting to save peer with updated token - ", i["token_peer"])
                peer.token = i["token_peer"]
                peer.last_updated = timezone.now()
                peer.save()
            except Exception as e:
                print("Error occured while saving peer - ", str(e))

        return Response(status=status.HTTP_200_OK)


class plates(APIView):
    permission_classes = (AllowAny,)

    # get all plates
    # TODO: add by time, etc
    def get(self, request):
        ip = get_ip(request)

        try:
            pass
            # TODO: why did I put token here
            # token = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            peer_object = models.peer_list.objects.all().filter(ip_address=ip)
        except models.peer_list.DoesNotExist or len(peer_object) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        trust_threshold = len(peer_object) * settings.TRUST_THRESHOLD
        trust_peer_object = 0
        for i in peer_object:
            trust_peer_object += i.trust

        if trust_peer_object >= trust_threshold:
            plates = models.plates.objects.all()
            serializer = serializers.get_plates(plates, many=True)
            return Response(dict(plates=serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_200_OK)

    # accept plates from other users
    def post(self, request):
        bootstrap_obj = models.bootstrap.objects.first()
        json_ret = {}

        if bootstrap_obj is None:
            # shoudln't happen as all peers should be registered to be peers, but who knows...
            # TODO: return fail, as not registered yet
            json_ret["status"] = "failure"
            json_ret["reason"] = "Peer is not registered yet, please ask them to do so."
            return Response(json_ret, status=status.HTTP_200_OK)
        else:
            self_token = bootstrap_obj.token_peer

        try:
            token = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            # TODO: return fail, no token included
            json_ret["status"] = "failure"
            json_ret["reason"] = "No peer token included."
            return Response(json_ret, status=status.HTTP_400_BAD_REQUEST)

        if token == self_token:
            json_data = json.loads(request.body.decode("utf-8"))

            plates_added = 0
            for i in json_data["plate_list"]:
                # get peer object first, then assign source to all plates from that peer
                # ignore integrity error
                ip_address = i["source"]["ip_address"]
                port = i["source"]["port"]
                try:
                    peer_obj = models.peer_list.objects.get(ip_address=ip_address, port=port)
                except ObjectDoesNotExist:
                    json_ret["status"] = "failure"
                    json_ret["reason"] = i["source"]["ip_address"] + "/" + i["source"][
                        "port"] + " not a recognized peer, verify IP/PORT combination."

                for j in i["plates"]:
                    try:
                        models.plates.objects.create(
                            # timestamp_recieved=,
                            timestamp_peer=j["timestamp_recieved"],
                            plate=j["plate"],
                            location_lat=j["location_lat"],
                            location_long=j["location_long"],
                            confidence=j["confidence"],
                            sent=False,
                            source=peer_obj,
                        )
                        plates_added += 1
                        peer_obj.no_plates += 1
                        peer_obj.save()
                    except IntegrityError:
                        print("Integrity Error for ", j["plate"])

            json_ret["status"] = "success"
            json_ret["reason"] = str(plates_added) + " added"
            return Response(json_ret, status=status.HTTP_200_OK)

        else:
            json_ret["status"] = "failure"
            json_ret["reason"] = "Wrong peer token."
            return Response(json_ret, status=status.HTTP_401_UNAUTHORIZED)
