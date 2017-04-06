from django.conf import settings
from django_cron import CronJobBase, Schedule

from django.utils import timezone

import requests, json, datetime

from client import models


class Keep_Alive(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.keep_alive'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL
        target_url = base_url + 'bootstrap/' + 'keep_alive/'
        # print(post_url)

        a = models.bootstrap.objects.first()
        token = a.token_update

        headers = {
            'Content-Type': 'application/json',
            'Authorization': token,
        }
        payload = {
            "ip_address": settings.PEER_HOSTNAME,
            "port": settings.PEER_PORT,
        }

        try:
            r = requests.post(base_url, data=json.dumps(payload), headers=headers)
            r.raise_for_status()
        except requests.RequestException as e:
            print("Exception raised at requests - ", e)
            print(r.status_code, r.json())

        a.last_updated = timezone.now()
        try:
            a.save()
        except Exception as e:
            print("Exception occured when saving - ", e, e.__cause__)


class Keep_Alive_Peer(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.keep_alive_peer'

    def do(self):
        peer_obj = models.peer_list.objects.all()

        peer_obj_self = peer_obj.filter(is_self=True).first()
        peer_obj = peer_obj.filter(is_self=False)

        for i in peer_obj:
            base_url = "http://" + str(i.ip_address) + ":" + str(i.port) + "/client/status/"
            token = str(i.token)

            headers = {
                'Content-Type': 'application/json',
                'Authorization': token,
            }

            payload = {
                "ip_address": str(peer_obj_self.ip_address),
                "port": peer_obj_self.port,
            }

            raised = False
            try:
                r = requests.post(base_url, data=json.dumps(payload), headers=headers)
                r.raise_for_status()
            except requests.RequestException as e:
                raised = True
                print("Exception raised at requests - ", e)
                print(r.status_code, r.json())

            if not raised:
                i.last_updated = timezone.now()
                try:
                    i.save()
                except Exception as e:
                    print("Exception occured when saving - ", e, e.__cause__)
