from django.conf import settings
from django_cron import CronJobBase, Schedule

import requests, json, datetime

from client import models

class Share_Plates(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.share_plates'

    def do(self):


        pass