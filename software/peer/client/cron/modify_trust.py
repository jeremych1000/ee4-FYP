from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.db import *
from django.db.utils import *
from django.core.exceptions import *
from django_cron import CronJobBase, Schedule
from django.db.models import Q

import requests, json, datetime, math
from difflib import SequenceMatcher
from operator import itemgetter

from client import models, serializers


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Modify_Trust(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.modify_trust'

    def do(self):
        print("Running Modify_Trust")

        try:
            peers = models.peer_list.objects.all()
            peer_self = peers.filter(is_self=True).first()
        except ObjectDoesNotExist:
            print("peer object does not exist")
            raise
        if not peer_self:
            print("peer object does not exist")
            raise
        print("Gotten peer_self")

        has_plates = True
        try:
            plates = models.plates.objects.all()
            #print("plates is ", plates)
        except ObjectDoesNotExist:
            print("plates object does not exist")
            has_plates = False
        if not plates:
            print("plates object does not exist")
            has_plates = False
        print("Gotten plates for trust")

        if has_plates:
            plates_self = plates.filter(source=peer_self)
            plates_others = plates.filter(~Q(source=peer_self))
            plates_others = plates_others.filter(processed_trust=False)

            pl_self = serializers.get_plates(plates_self, many=True)
            pl_others = serializers.get_plates(plates_others, many=True)

            pl_self_json = json.loads(json.dumps(pl_self.data, indent=2))
            pl_others_json = json.loads(json.dumps(pl_others.data, indent=2))

            # loop other plate then loop inner plate
            pl_self_list = [i["plate"] for i in pl_self_json]
            pl_others_list = [i["plate"] for i in pl_others_json]

            pl_in_both = [i for i in pl_others_list if i in pl_self_list]

            others_with_matching_plates = []

            for i in pl_in_both:
                try:
                    others_plate = plates_others.filter(plate=i).last()
                except ObjectDoesNotExist:
                    print("Object does not exist")
                others_plate_source = others_plate.source

                others_plate_source.trust += settings.ADD_TRUST_MATCHING_PLATE
                others_plate_source.no_matching_plates += 1
                others_plate_source.save()
                others_with_matching_plates.append(others_plate_source)

                others_plate.processed_trust = True
                others_plate.save()

            decrease_trust_peers = [i for i in peers if i not in others_with_matching_plates]
            print(decrease_trust_peers)
            for i in decrease_trust_peers:
                if i.no_plates > 0 and i.trust > 0:
                    i.trust = math.floor(i.trust * settings.TRUST_DECAY)
                    i.save()
