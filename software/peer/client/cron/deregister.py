from django.conf import settings
from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models


class Deregister(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.deregister'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL
        target_url = base_url + 'bootstrap/' + 'deregister/'

        token = models.bootstrap.objects.first().token_update
        print(token)
        headers = {
            'Authorization': token,
        }
        payload = {
            "ip_address": settings.PEER_HOSTNAME,
            "port": settings.PEER_PORT,
        }

        r = requests.post(target_url, data=json.dumps(payload), headers=headers)
        print(r.text)

        if r.status_code == 200:
            models.bootstrap.objects.all().delete()  # delete existing bootstrapped record
        else:
            print("Something went wrong, HTTP status: ", r.status_code)
