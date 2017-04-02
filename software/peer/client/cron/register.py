from django.conf import settings

from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models


class Register(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.register'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL
        post_url = base_url + 'bootstrap/' + 'register/'

        print(post_url)

        payload = {
            "ip_address": "peer1",
            "port": 34571,
        }

        r = requests.post(post_url, data=json.dumps(payload))
        print(r.text)

        models.bootstrap.objects.create(
            token_update=r.json()["token_update"],
            token_peer=r.json()["token_peer"],
            last_updated=datetime.datetime.now(),
        )
