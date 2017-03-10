from django.db import models


class bootstrap(models.Model):
    token_update = models.CharField(max_length=40)
    token_peer = models.CharField(max_length=40)
    time_accepted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)


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

    first_seen = models.DateTimeField(
        auto_now_add=True)  # Automatically set the field to now when the object is first created.
    last_seen = models.DateTimeField(auto_now_add=False, auto_now=True)

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

    first_seen = models.DateTimeField(
        auto_now_add=True)  # Automatically set the field to now when the object is first created.
    last_seen = models.DateTimeField(auto_now_add=False, auto_now=True)

    img_path = models.FilePathField()
