from django.core.management.base import BaseCommand
from django.conf import settings

import requests, json, datetime

from client import models

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        base_url = settings.BOOTSTRAP_BASE_URL

        payload = {
            "ip_address": "86.166.168.90",
            "port": 34572,
        }

        r = requests.post(base_url+'bootstrap/'+'register/', data=json.dumps(payload))

        models.bootstrap.objects.create(
            token_update = r.json()["token_update"],
            token_peer = r.json()["token_peer"],
            last_updated = datetime.datetime.now(),
        )