from rest_framework import serializers
from . import models


class peer(serializers.ModelSerializer):
    class Meta:
        # query returns FeatureEntry objects
        model = models.peer
        fields = (
            'ip_address', 'port', 'location_lat', 'location_long', 'location_city', 'location_country', 'first_seen',
            'last_seen', 'token_update', 'token_peer', 'active',)
