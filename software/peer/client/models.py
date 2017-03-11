from django.db import models
from django.utils import timezone

class bootstrap(models.Model):
    # prevent more than one entry
    ajsdkfjasldkfjasldkfja = models.CharField(max_length=1, default="1", unique=True)
    token_update = models.CharField(max_length=40)
    token_peer = models.CharField(max_length=40)
    time_accepted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField()


class plates(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    plate = models.CharField(max_length=10)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                       null=True)  # rough location to organize peers by proximity
    location_long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                        null=True)  # rough location to organize peers by proximity
    confidence = models.FloatField()


class peer_list(models.Model):
    ip_address = models.GenericIPAddressField(protocol='ipv4')  # reachable IP address
    port = models.PositiveIntegerField()  # port on which server is run on

    time_accepted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField()

    token = models.UUIDField(default=None,
                             editable=False)

    active = models.BooleanField(default=False)

    no_plates = models.PositiveIntegerField()

    no_matching_plates = models.PositiveIntegerField()

    trust = models.PositiveIntegerField()


class violations(models.Model):
    plate1 = models.ForeignKey(plates, related_name='plate1')
    plate2 = models.ForeignKey(plates, related_name='plate2')

    average_speed = models.FloatField()
    unit = models.CharField(default="miles", max_length=5)
    method = models.CharField(default="p2p", max_length=10)  # or itself

    time_accepted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField()

    img_path = models.FilePathField()
