from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from django_cron import CronJobBase, Schedule

from bootstrap import models

class Minutes_Connected(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bootstrap.minutes_connected'

    def do(self):
        peer_objects = models.peer.objects.all()

        for i in peer_objects:
            if i.active == True:
                i.minutes_connected += 5
                i.save()