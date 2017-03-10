from rest_framework import serializers
from . import models


class get_plates(serializers.ModelSerializer):
    class Meta:
        model = models.plates
        fields = (
                'timestamp', 'plate', 'location_lat', 'location_long', 'confidence',
            )
