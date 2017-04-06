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

        peers = models.peer.objects.all()
        try:
            peer_objects = peers.filter(requires_peer_broadcasting=True)
        except ObjectDoesNotExist:
            need_broadcasting = False

        if need_broadcasting:
            serializer = serializers.get_token(peer_objects,  many=True)

            try:
                peer_objects = peers.filter(active=True, requires_peer_broadcasting=False)
            except ObjectDoesNotExist:
                print("No active peers found")

            for i in peer_objects:
                target_url = 'http://' + str(i.ip_address) + ':' + str(i.port) + '/client/peers/'
                headers = {
                    'Content-Type': 'application/json'
                }
                payload = {
                    'peers': serializer.data
                }

                raised = False
                try:
                    r = requests.patch(target_url, data=json.dumps(payload), headers=headers)
                    r.raise_for_status()
                except requests.RequestException as e:
                    raised=True
                    print("Requests exception - ", str(e), " for peer ", target_url)
                except Exception as e:
                    raised=True
                    print("Exception during requests - ", str(e), " for peer ", target_url)

                if not raised:
                    print("No problem, resetting requires_peer_broadcasting")
                    i.requires_peer_broadcasting = False
                    try:
                        i.save()
                    except Exception as e:
                        print("Exception occured while saving - ", str(e))

                        