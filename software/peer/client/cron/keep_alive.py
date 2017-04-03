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
        print(post_url)

        a = models.bootstrap.objects.first()
        token = a.token_update

        headers = {
            'Content-Type': 'application/json',
            'Authorization': token,
        }
        payload = {
            "ip_address": "peer1",
            "port": 34571,
        }

        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        print(r.text)

        a.last_updated = timezone.now()
        a.save()
