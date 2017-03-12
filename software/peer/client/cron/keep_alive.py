from django.conf import settings
from django.utils import timezone

from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models


class Keep_Alive(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.keep_alive'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL

        bootstrap_server = models.bootstrap.objects.all().first()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': bootstrap_server.token_update,
        }
        payload = {
            "ip_address": "86.166.168.90",
            "port": 34568,
        }

        r = requests.post(base_url + 'bootstrap/' + 'keep_alive/', data=json.dumps(payload), headers=headers)
        print(r.text)

        bootstrap_server.last_updated = timezone.now()
        bootstrap_server.save()
