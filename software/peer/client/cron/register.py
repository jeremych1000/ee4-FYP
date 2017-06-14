from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.db import *
from django.db.utils import *
from django.core.exceptions import *

import requests, json, datetime

from client import models
from client.encrypt import encrypt, decrypt


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

        if models.bootstrap.objects.count() == 0:
            # try to delete server bootstrap first, only if locally haven't registered
            r = requests.delete(target_url, data=encrypt(json.dumps(payload), settings.FERNET_KEY))
            if r.status_code == 400:
                print("Bootstrap cant find peer object, so assume all deleted")
            else:
                r.raise_for_status()

        r = requests.post(target_url, data=encrypt(json.dumps(payload), settings.FERNET_KEY))

        if r.status_code == 201:
            models.bootstrap.objects.all().delete()  # delete existing bootstrapped record
            models.bootstrap.objects.create(
                token_update=r.json()["token_update"],
                token_peer=r.json()["token_peer"],
            )
            print("Bootstrap object created")
        elif r.status_code == 409:  # conflict:
            print("409 conflict, now patching for new key")
            try:
                b = models.bootstrap.objects.first()
            except ObjectDoesNotExist:
                print("No bootstrap object found, please delete record in bootstrap server.")

            print("Bootstrap object found, now issuing PATCH")
            payload = {
                "ip_address": settings.PEER_HOSTNAME,
                "port": settings.PEER_PORT,
                "token_update": str(b.token_update),
                "token_peer": str(b.token_peer),
            }

            try:
                r = requests.patch(target_url, data=encrypt(json.dumps(payload), settings.FERNET_KEY))
                r.raise_for_status()
            except requests.RequestException as e:
                print("Requests exception - ", str(e))

            print("patch old is ", b.token_update, b.token_peer)
            print("patch json is ", r.json())
            b.token_update = r.json()["token_update"]
            b.token_peer = r.json()["token_peer"]
            try:
                b.save()
            except Exception as e:
                print("Exception occured while saving while PATCHing - ", str(e))

            # update peer list record too if exist
            try:
                p = models.peer_list.objects.get(is_self=True)
            except ObjectDoesNotExist:
                print(
                    "Peer list object does not, which shouldn't happen since it should only exist if we have registered!")

            p.token = r.json()["token_peer"]
            p.last_updated = timezone.now()
            try:
                p.save()
            except Exception as e:
                print("Exception occured while saving peer list record - ", str(e))

            print("Successfully updated bootstrap and peer_lists.")
        else:
            print("Other HTTP status code recieved - ", r.status_code)
