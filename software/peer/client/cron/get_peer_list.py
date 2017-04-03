from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.db import *
import requests, json, datetime

from client import models


class Get_Peer_List(CronJobBase):
    RUN_EVERY_MINS = 15
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.get_peer_list'

    def do(self):
        base_url = settings.BOOTSTRAP_BASE_URL
        target_url = base_url + 'bootstrap/' + 'get_peer_list/'

        # add auth later
        # token = models.bootstrap.objects.first().token_update

        r = requests.get(target_url)
        json_ret = r.json()

        # TODO this is not very elegant, delete all
        models.peer_list.objects.all().delete()

        total_added = 0
        for i in json_ret:
            try:
                models.peer_list.objects.create(
                    ip_address=i["ip_address"],
                    port=i["port"],
                    location_lat=i["location_lat"],
                    location_long=i["location_long"],
                    location_city=i["location_city"],
                    location_country=i["location_country"],
                    # time_accepted=
                    # last_updated=
                    token=i["token_peer"],
                    active=i["active"],
                    # no_plates=
                    # no_matching_plates=
                    # trust=
                )
                total_added += 1
            except Exception as e:
                print(e.__cause__)

        print("Total peers added: ", total_added)
        pass
