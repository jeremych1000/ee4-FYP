'''
TODO

add /client/violations/ URL and POST view
add allauth social, testing posting on social networks
add social model for successful violations
link ALPR with file saving (check file size?) for self detecting violations
go to violations.py, CTRL+F TODO
find out what is django model index_together (django cron uses it) (utilizes db_index in fields?)
'''

from django.conf import settings
from django.utils import timezone
from django.db import *
from django.db.utils import *
from django.core.exceptions import *

from django_cron import CronJobBase, Schedule, models

import requests, json, datetime

from client import models


class Detect_Violations(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.detect_violations'

    def do(self):

        # TODO add null to plate 2 for self method

        # start_time = models.DateTimeField(db_index=True)
        # end_time = models.DateTimeField(db_index=True)
        # is_success = models.BooleanField(default=False)
        last_run = models.CronJobLog.objects.last().end_time
        time_now = timezone.now()
        delta = datetime.timedelta(last_run, time_now)

        try:
            peer_self = models.peer_list.objects.get(is_self=True)
        except ObjectDoesNotExist:
            print("Exception occured at finding peer_self - object does not exist.")
            return  # does this work?
        plates = models.plates.objects.all().filter(
            timestamp_peer__gte=last_run)  # get plates that are fresher than last run time

        plates_self = plates.filter(source=peer_self)
        # plates_peer = plates that are not from peer_self
        plates_peer = plates

        process = True
        process_using_self = False
        if len(plates_peer) == 0:
            process_using_self = True
            print("There are no plates from peers to process.")
        elif len(plates_self) == 0:
            process = False
            print("There are no plates from self to process.")

        if process:
            if not process_using_self:
                for i in plates_peer:
                    if i in plates_self:
                        j = plates_self.get(i)
                        # TODO: add google distance API URL in settings
                        # TODO: add google API key in settings
                        base_url = settings.GOOGLE_API_DISTANCE + settings.API_KEY + 'distance_between' + \
                                   i.location_lat + i.location_long + j.location_lat + j.location_long
                        # check for avg speed

                        try:
                            r = requests.post(base_url)  # payload? headers?
                            r.raise_for_status()
                        except requests.RequestException as e:
                            print("Exception occursed while trying to consult the Google Maps API - ", e)

                        assert (r.status_code == 200)
                        json_ret = r.json()

                        g_api_distance = json_ret["distance"]  # TODO <- change
                        g_api_speed_limit = json_ret["speed_limit"]  # TODO <- maybe request another URL

                        time_between = abs(i.timestamp_peer - j.timestamp_peer)

                        speed = g_api_distance / time_between
                        if speed > (g_api_speed_limit * (1 + settings.SPEED_LIMIT_OVER / 100)):  # TODO <- change
                            try:
                                models.violations.create(
                                    plate1=i,  # models.ForeignKey(plates, related_name='plate1')
                                    plate2=j,  # models.ForeignKey(plates, related_name='plate2')
                                    average_speed=speed,  # models.FloatField()
                                    unit=settings.SPEED_UNIT,
                                    # TODO <- add to settings # models.CharField(default="miles", max_length=5)
                                    method='p2p',  # models.CharField(default="p2p", max_length=10)  # or itself
                                    time_accepted=timezone.now(),  # models.DateTimeField(default=timezone.now)
                                    # TODO last_updated=, # models.DateTimeField()
                                    # TODO img_path=, # models.FilePathField()
                                )
                            except IntegrityError:
                                print("Integrity error for plate ", i.plate, " ", j.plate)
                            except Exception as e:
                                print("Exception occured while saving to database - ", e)

                            print("Violation of " + i.plate + " added to the database.")
                            # TODO notify user?
                            # TODO notify peers

                            # after adding to violations, then contact peer to tell them violated
                            # double check if possible?
                            # TODO add social post model

                            peer_social_url = 'http://' + j.source.ip_address + ':' + j.source.port + '/client/violations/'
                            headers = {
                                'Content-Type': 'application/json',
                                'Authorization': str(j.source.token)
                            }
                            # TODO add payload
                            payload = {
                                'a': 1
                            }
                            try:
                                r = requests.post(peer_social_url, data=json.dumps(payload), headers=headers)
                            except requests.RequestException as e:
                                print("Exception occured at requesting peer social URL - ", e)


            else:
                # process using self
                # TODO tie this to OpenALPR, whenever a plate is detected then make another model
                # make another model with foreign key to save the detailed regions, link to plates model
                # batch it up for not stalling CPU
                # if speed > something, then add to violations
                # then notify user?
                pass
        else:
            print("Not processing, exiting.")
