from django.conf import settings
from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models, serializers


class Share_Plates(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.share_plates'

    def do(self):
        plates_to_be_sent = models.plates.objects.filter(sent=False)
        print(plates_to_be_sent)
        if len(plates_to_be_sent) >= settings.NO_PLATES_BATCH_BEFORE_SEND:
            peer_self = models.peer_list.objects.get(is_self=True)
            active_peers = models.peer_list.objects.filter(active=True, is_self=False) #, trust__gte=settings.TRUST_THRESHOLD)

            for i in active_peers:
                base_url = 'http://' + i.ip_address + ':' + str(i.port) + '/client/plates/'
                token = str(i.token)
                print(base_url, token)
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                }

                plates = serializers.get_plates(models.plates.objects, many=True)

                payload = {
                    "ip_address": settings.PEER_HOSTNAME,
                    "port": settings.PEER_PORT,
                    "plates": plates.data
                }

                try:
                    r = requests.post(base_url, data=json.dumps(payload), headers=headers)
                    r.raise_for_status()
                    print(r.json())
                except requests.RequestException as e:
                    raised = True
                    print(r.status_code, r.json())
                assert(r.status_code==200)