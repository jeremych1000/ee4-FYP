from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from django_cron import CronJobBase, Schedule

import requests, json, datetime

from bootstrap import models


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    total_hours = hours + minutes / 60 + (seconds / 60) / 60
    total_minutes = 60 * hours + minutes + seconds / 60
    return hours, minutes, seconds, total_hours, total_minutes


class Prune_Alive(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bootstrap.prune_alive'

    def do(self):
        peer_objects = models.peer.objects.all()

        for i in peer_objects:
            t_delta =  timezone.now() - i.last_seen
            hours, minutes, seconds, total_hours, total_minutes = convert_timedelta(t_delta)
            # print(hours, " ", minutes, " ", seconds, " ", total_hours, " ", total_minutes)

            if total_minutes >= 10:
                i.active = False
                i.save()
                print("made inactive")
            if total_hours >= 24:
                i.delete()
                print("deleted")
