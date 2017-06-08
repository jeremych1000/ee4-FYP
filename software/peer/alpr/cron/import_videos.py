from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.db import *
from django.core.exceptions import *

import requests, json, datetime, os

from alpr import models


class Import_Videos(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'alpr.import_videos'

    def do(self):
        filelist = [f for f in os.listdir(settings.ALPR_VIDEO_PATH) if
                    os.path.isfile(os.path.join(settings.ALPR_VIDEO_PATH, f))]

        print(type(filelist), filelist)

        for file in filelist:
            try:
                models.videos.objects.create(
                    filename=os.path.join(settings.ALPR_VIDEO_PATH, file),
                    processed=False,
                    time_processed=timezone.make_aware(datetime.datetime.utcfromtimestamp(0)),
                )
            except IntegrityError:
                print("Integrity Error, setting to not processed.")
                a = models.videos.objects.get(filename=os.path.join(settings.ALPR_VIDEO_PATH, file))
                a.processed = False
                try:
                    a.save()
                except Exception as e:
                    print("Exception while saving while integrity error - ", str(e))
