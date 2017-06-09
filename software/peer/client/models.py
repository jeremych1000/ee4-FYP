from django.db import models
from django.utils import timezone

from datetime import datetime


class bootstrap(models.Model):
    # what a crappy method of preventing more than one entry... should use admin methods in the future
    # but hey it works
    asdf = models.CharField(max_length=1, default="1", unique=True, editable=False)

    token_update = models.CharField(max_length=40)
    token_peer = models.CharField(max_length=40)
    time_accepted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.make_aware(datetime.utcfromtimestamp(0)))


class peer_list(models.Model):
    ip_address = models.GenericIPAddressField(protocol='ipv4')  # reachable IP address
    port = models.PositiveIntegerField()  # port on which server is run on
    is_self = models.BooleanField(default=False) # self is protected keyword, dont use that

    location_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                       null=True)  # rough location to organize peers by proximity
    location_long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                        null=True)  # rough location to organize peers by proximity
    location_city = models.CharField(max_length=50, blank=True, default=None,
                                     null=True)  # HIDDEN FROM USER, holds rough city from IP geolocation
    location_country = models.CharField(max_length=50, blank=True, default=None,
                                        null=True)  # HIDDEN FROM USER, holds rough country from IP geolocation

    time_accepted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(
        default=timezone.make_aware(datetime.utcfromtimestamp(0)))  # I assume this means epoch

    token = models.UUIDField(default=None,
                             editable=False)

    active = models.BooleanField(default=False)

    no_plates = models.PositiveIntegerField(default=0)

    no_matching_plates = models.PositiveIntegerField(default=0)

    trust = models.FloatField(default=500)

    class Meta:
        # http://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
        # unique tuple
        unique_together = ('ip_address', 'port')


class plates(models.Model):
    timestamp_recieved = models.DateTimeField(default=timezone.now) # for when recieve the plate
    timestamp_peer = models.DateTimeField(default=timezone.make_aware(datetime.utcfromtimestamp(0)))
    plate = models.CharField(max_length=10)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                       null=True)  # rough location to organize peers by proximity
    location_long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                        null=True)  # rough location to organize peers by proximity
    confidence = models.FloatField(default=0)
    source = models.ForeignKey(peer_list, default=None)

    sent = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('timestamp_peer', 'plate')


class violations(models.Model):
    plate1 = models.ForeignKey(plates, related_name='plate1')
    plate2 = models.ForeignKey(plates, related_name='plate2')

    average_speed = models.FloatField()
    unit = models.CharField(default="miles", max_length=5)
    method = models.CharField(default="p2p", max_length=10)  # or itself

    time_accepted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.make_aware(datetime.utcfromtimestamp(0)))

    img_path = models.FilePathField()
