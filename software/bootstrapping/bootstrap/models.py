from django.db import models

import uuid


# Create your models here.
class peer(models.Model):
    ip_address = models.GenericIPAddressField(protocol='ipv4')  # reachable IP address
    port = models.PositiveIntegerField()  # port on which server is run on

    location_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                       null=True)  # rough location to organize peers by proximity
    location_long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=None,
                                        null=True)  # rough location to organize peers by proximity
    location_city = models.CharField(max_length=50, blank=True, default=None,
                                     null=True)  # HIDDEN FROM USER, holds rough city from IP geolocation
    location_country = models.CharField(max_length=50, blank=True, default=None,
                                        null=True)  # HIDDEN FROM USER, holds rough country from IP geolocation

    first_seen = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    last_seen = models.DateTimeField(auto_now_add=False, auto_now=True)

    # NOT default=uuid.uuid4 as only populate UUID from register view as need to return the value
    token_update = models.UUIDField(default=None,
                                    editable=False)  # token to update this peer entry to prevent random post requests to update entry

    token_peer = models.UUIDField(default=None,
                                  editable=False)  # token which will be distributed to other peers to allow token authentication when communicating

    active = models.BooleanField(default=False)

    class Meta:
        # http://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
        # unique tuple
        unique_together = ('ip_address', 'port')