from django.core.management.base import BaseCommand
from django.conf import settings

import requests, json, datetime

from bootstrap import models

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        peer_objects = models.peer.objects.all()

        for i in peer_objects:
            t_delta = i.last_seen - i.first_seen
            print(i.ip_address, i.port, t_delta)