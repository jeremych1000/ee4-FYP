from django.db import models
from django.utils import timezone
from django.conf import settings

from datetime import datetime

class videos(models.Model):
    # what a crappy method of preventing more than one entry... should use admin methods in the future
    # but hey it works
    filename = models.FilePathField(path=settings.ALPR_VIDEO_PATH, unique=True, match="*.mp4", allow_folders=False, recursive=True)
    processed = models.BooleanField(default=False)
    time_processed = models.DateTimeField(default=None, null=True)