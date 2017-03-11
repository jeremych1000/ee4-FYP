from django_cron import CronJobBase, Schedule
from django.conf import settings

import requests, json, datetime

from client import models


class Register(CronJobBase):
    RUN_EVERY_MINS = 0
    schedule = Schedule(run_at_times=RUN_EVERY_MINS)
    code = 'peer.register'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL

        payload = {
            "ip_address": "86.166.168.90",
            "port": 34568,
        }

        r = requests.post(base_url + 'bootstrap/' + 'register/', data=json.dumps(payload))
        print(r.text)

        models.bootstrap.objects.create(
            token_update=r.json()["token_update"],
            token_peer=r.json()["token_peer"],
            last_updated=datetime.datetime.now(),
        )
