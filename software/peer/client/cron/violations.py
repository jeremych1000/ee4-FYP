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
from django.db.models import Q

from django_cron import CronJobBase, Schedule, models

import requests, json, datetime, googlemaps

from client import models, serializers


def get_distance(origin, destination):
    # returns distance for driving directions in metres
    # ignore estimated driving time, just get road distance
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    ret = gmaps.distance_matrix(origins=origin, destinations=destination, units="imperial")
    # print(json.dumps(ret, indent=2))
    return ret["rows"][0]["elements"][0]["distance"]["value"]


def is_speeding(distance, timedelta, leeway=10):
    # leeway is how much above speed limit count as not speeding
    # speed = distance / time
    # time is in seconds, convert to hour
    # distance is in m, convert to miles/hour
    speed = 2.25 * (distance / timedelta)
    max_speed = settings.RESIDENTIAL_SPEED_LIMIT * (1 + (settings.SPEEDING_LIMIT_PERCENT / 100))
    return (speed > max_speed, speed)


class Detect_Violations(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.detect_violations'

    def do(self):
        try:
            peers = models.peer_list.objects.all()
            peer_self = peers.filter(is_self=True).first()
        except ObjectDoesNotExist:
            print("peer object does not exist")
            raise
        if not peer_self:
            print("peer object does not exist")
            raise

        has_plates = True
        try:
            plates = models.plates.objects.all()
            print("plates is ", plates)
        except ObjectDoesNotExist:
            print("plates object does not exist")
            has_plates = False
        except Exception as e:
            print(str(e))
        if not plates:
            print("plates object does not exist")
            has_plates = False
        print("Gotten plates")

        if has_plates:
            plates_self = plates.filter(source=peer_self)
            plates_others = plates.filter(~Q(source=peer_self))
            plates_others = plates_others.filter(processed_violation=False)

            pl_self = serializers.get_plates(plates_self, many=True)
            pl_others = serializers.get_plates(plates_others, many=True)

            pl_self_json = json.loads(json.dumps(pl_self.data, indent=2))
            pl_others_json = json.loads(json.dumps(pl_others.data, indent=2))

            # loop other plate then loop inner plate
            pl_self_list = [i["plate"] for i in pl_self_json]
            pl_others_list = [i["plate"] for i in pl_others_json]

            pl_in_both = [i for i in pl_others_list if i in pl_self_list]

            for i in pl_in_both:
                self_plate = plates_self.filter(plate=i).last()
                others_plate = plates_others.filter(plate=i).last()

                timedelta = abs(self_plate.timestamp - others_plate.timestamp).total_seconds()

                distance = get_distance((self_plate.location_lat, self_plate.location_long),
                                        (others_plate.location_lat, others_plate.location_long))

                try:
                    speeding, speed = is_speeding(distance, timedelta)
                except Exception as e:
                    print(str(e))
                print(self_plate.plate, " is ", ("" if speeding else "not"), " speeding based on travelling ", distance,
                      " in ", timedelta, "seconds, equating to ", speed, " miles per hour")

                if speeding:
                    success = True
                    try:
                        models.violations.objects.create(
                            plate1=self_plate,
                            plate2=others_plate,
                            average_speed=speed,
                            time1=self_plate.timestamp,
                            time2=others_plate.timestamp,
                            distance=distance,
                        )
                    except IntegrityError:
                        print("Integrity error for ", self_plate.plate)
                        success = False
                    except Exception as e:
                        print(str(e))
                        success = False
                if success:
                    print("Successfully added to violations database")
                    others_plate.processed_violation = True
                    others_plate.save()
