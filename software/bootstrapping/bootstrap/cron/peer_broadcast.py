from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import *
from django.db import *
from django_cron import CronJobBase, Schedule

from bootstrap import models, serializers

import requests, json

class Update_Tokens(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bootstrap.update_tokens'

    def do(self):
        need_broadcasting = True
        try:
            peer_objects = models.peer.objects.filter(requires_peer_broadcasting=True)
        except ObjectDoesNotExist or len(peer_objects) == 0:
            need_broadcasting = False

        if need_broadcasting:
            serializer = serializers.get_token(peer_objects,  many=True)

            for i in peer_objects:
                target_url = 'http://' + i.ip_address + ':' + i.port + '/client/peers/'
                headers = {
                    'Content-Type': 'application/json'
                }
                payload = {
                    'peers': serializer.data
                }

                try:
                    r = requests.patch(target_url, data=json.dumps(payload), headers=headers)
                    r.raise_for_status()
                except requests.RequestException as e:
                    print("Requests exception - ", str(e), " for peer ", target_url)
                except Exception as e:
                    print("Exception during requests - ", str(e), " for peer ", target_url)

                i.requires_peer_broadcasting = False
                try:
                    i.save()
                except Exception as e:
                    print("Exception occured while saving - ", str(e))