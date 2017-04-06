from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.db import *
from django.core.exceptions import *

import requests, json, datetime

from client import models


class Check_Violations(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'peer.check_violations'

    def do(self):
        pass