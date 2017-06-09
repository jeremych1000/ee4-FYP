from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.db import *
from django.db.utils import *
import requests, json, datetime

from client import models

class Get_Peer_List(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.get_peer_list'

    def do(self):
        if models.bootstrap.objects.count() == 0:
            print("PLEASE RUN B1.SH FIRST TO REGISTER.")
        else:
            base_url = settings.BOOTSTRAP_BASE_URL
            target_url = base_url + 'bootstrap/' + 'get_peer_list/'

            # add auth later
            # token = models.bootstrap.objects.first().token_update

            r = requests.get(target_url)
            json_ret = r.json()
            print("No. of peers recieved: ", len(json_ret))

            # TODO this is not very elegant, delete all
            models.peer_list.objects.all().delete()

            total_added = 0
            for i in json_ret:
                print(i)

                is_self = (i["ip_address"] == settings.PEER_HOSTNAME and i["port"] == settings.PEER_PORT)

                status_url = "http://" + str(i["ip_address"]) + ":" + str(i["port"]) + "/client/state/"
                try:
                    r = requests.get(status_url)
                    r.raise_for_status()
                except requests.RequestException as e:
                    print("Exception while requests - ", e.request, e.response, e.__cause__)

                active = (r.status_code == 200)  # <- leave this for pinging by peer, ignore bootstrap active

                try:
                    models.peer_list.objects.create(
                        ip_address=i["ip_address"],
                        port=i["port"],
                        is_self=is_self,
                        location_lat=i["location_lat"],
                        location_long=i["location_long"],
                        location_city=i["location_city"],
                        location_country=i["location_country"],
                        # time_accepted=
                        # last_updated=
                        token=i["token_peer"],
                        active=active,
                        # no_plates=
                        # no_matching_plates=
                        # trust=
                    )
                    total_added += 1
                except Exception as e:
                    print("Exception while adding to database - ", e.__cause__)

            print("Total peers added: ", total_added)
