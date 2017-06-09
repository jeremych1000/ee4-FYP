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

from client import models, serializers


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

        try:
            plates = models.plates.objects.all()
            print("plates is ", plates)
        except ObjectDoesNotExist:
            print("plates object does not exist")
            raise
        if not plates:
            print("plates object does not exist")
            raise
        print("Gotten plates")

        plates_self = plates.filter(source=peer_self)
        plates_others = plates.filter(~Q(source=peer_self))
        plates_others = plates_others.filter(processed=False)

        in_plates_self = []
        for i in plates_others:
            if i in plates_self:
                source = i.source
                source.trust += settings.ADD_TRUST_MATCHING_PLATE
                source.no_matching_plates += 1
                source.save()

                i.processed = True
                i.save()

                in_plates_self.append(source)

        for i in peers:
            if i not in in_plates_self and i is not peer_self:
                # only decrease trust if no plate from source in non-processed
                if i.no_plates > 0 and i.trust > 0:
                    i.trust = math.floor(i.trust * settings.TRUST_DECAY)
                    i.save()
