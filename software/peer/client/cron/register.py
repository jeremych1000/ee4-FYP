from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.utils import timezone

import requests, json, datetime

from client import models


class Register(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.register'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL
        target_url = base_url + 'bootstrap/' + 'register/'

        payload = {
            "ip_address": settings.PEER_HOSTNAME,
            "port": settings.PEER_PORT,
        }

        r = requests.post(target_url, data=json.dumps(payload))
        print(r.text)

        models.bootstrap.objects.all().delete()  # delete existing bootstrapped record

        models.bootstrap.objects.create(
            token_update=r.json()["token_update"],
            token_peer=r.json()["token_peer"],
            # last_updated=timezone.make_aware(datetime.datetime.now()),
        )
