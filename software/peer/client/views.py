from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse

import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

@login_required
def log(request):
    path = os.path.join(settings.STATICFILES_DIRS[0], 'log.log')
    # print(path)
    with open(path, 'r') as myfile:
        data=myfile.read()
    return HttpResponse(data, content_type='text/plain')


