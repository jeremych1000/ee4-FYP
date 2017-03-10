from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

import os, requests
from ipware.ip import get_ip

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import models, serializers

class get_plates(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        ip = get_ip(request)

        token = request.META['HTTP_AUTHORIZATION']

        try:
            peer_object = models.peer_list.objects.all().filter(ip_address=ip)
        except models.peer_list.DoesNotExist or len(peer_object) == 0:
            return Response(None, status=status.HTTP_200_OK)

        trust_threshold = len(peer_object) * settings.TRUST_THRESHOLD
        trust_peer_object = 0
        for i in peer_object:
            trust_peer_object += i.trust

        if trust_peer_object >= trust_threshold:
            plates = models.plates.objects.all()

            serializer = serializers.get_plates(plates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_200_OK)

