from django.conf import settings
from django.utils import timezone

from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models


class Keep_Alive(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.keep_alive'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL
        post_url = base_url + 'bootstrap/' + 'keep_alive/'

        bootstrap_server = models.bootstrap.objects.all().first()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': bootstrap_server.token_update,
        }
        payload = {
            "ip_address": "peer1",
            "port": 34571,
        }

        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        print(r.text)

        bootstrap_server.last_updated = timezone.now()
        bootstrap_server.save()
