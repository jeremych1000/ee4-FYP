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

import requests, json, datetime

from client import models, serializers


class Modify_Trust(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.modify_trust'

    def do(self):
        try:
            plates = models.plates.objects.all()
        except ObjectDoesNotExist:
            print("plates object does not exist")

        try:
            peer_self = models.peer_list.objects.all().filter(is_self=True).first()
        except ObjectDoesNotExist:
            print("peer object does not exist")

        plates_self = plates.filter(source=peer_self)
        plates_others = plates.filter(~Q(source=peer_self))
        plates_others = plates_others.filter(processed=False)

        not_in_plates_self = []
        for i in plates_others:
            if i in plates_self:
                source = i.source
                source.trust += 10
                source.no_matching_plates += 1
                i.processed = True

                source.save()
                i.save()
            else:
                if i not in not_in_plates_self:
                    not_in_plates_self.append(i.source)

        for i in not_in_plates_self:
            i.trust *= 0.9

