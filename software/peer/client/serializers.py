from rest_framework import serializers
from . import models


class get_plates(serializers.ModelSerializer):
    class Meta:
        model = models.plates
        fields = (
                'timestamp', 'plate', 'location_lat', 'location_long', 'confidence',
            )


class get_source(serializers.ModelSerializer):
    class Meta:
        model = models.peer_list
        fields = (
                'ip_address', 'port',
            )