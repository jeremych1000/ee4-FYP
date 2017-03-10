from django.core.management.base import BaseCommand
from django.conf import settings

import requests, json

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
        print(r.text)

