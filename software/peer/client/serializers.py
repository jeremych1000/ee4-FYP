from rest_framework import serializers
from . import models

import math

import django_tables2 as tables
from django_tables2.utils import A

class get_plates(serializers.ModelSerializer):
    class Meta:
        model = models.plates
        fields = (
                'timestamp', 'plate', 'location_lat', 'location_long', 'confidence',
            )

class get_plates_only(serializers.ModelSerializer):
    class Meta:
        model = models.plates
        fields = (
                'plate',
            )


class get_source(serializers.ModelSerializer):
    class Meta:
        model = models.peer_list
        fields = (
                'ip_address', 'port',
            )

class dashboard_bootstrap(serializers.ModelSerializer):
    class Meta:
        model = models.bootstrap
        fields = (
            'token_update', 'token_peer', 'time_accepted', 'last_updated',
        )

class dashboard_peer(serializers.ModelSerializer):
    class Meta:
        model = models.peer_list
        fields = (
            'ip_address',
            'port',
            'is_self',
            'location_lat',
            'location_long',
            'location_city',
            'location_country',
            'time_accepted',
            'last_updated',
            'token',
            'active',
            'no_plates',
            'no_matching_plates',
            'trust',
        )

class dashboard_plates(serializers.ModelSerializer):
    class Meta:
        model = models.plates
        fields = (
                'timestamp', 'plate', 'location_lat', 'location_long', 'confidence', 'img_path', 'processed_violation', 'sent'
            )

class dashboard_violations(serializers.ModelSerializer):
    p1 = serializers.ReadOnlyField(source='plate1.plate', read_only=True)
    p2 = serializers.ReadOnlyField(source='plate2.plate', read_only=True)

    class Meta:
        model = models.violations
        fields = (
            'p1',
            'p2',
            'average_speed',
            'unit',
            'method',
            'time1',
            'time2',
            'distance',
            'user_sent_to_peers',
        )

class table_bootstrap(tables.Table):
    token_peer = tables.Column()
    token_update = tables.Column()
    time_accepted = tables.Column()
    last_updated = tables.Column()

    class Meta:
        attrs = {'class': 'table table-striped'}

class table_peers(tables.Table):
    ip_address = tables.Column()
    port = tables.Column()
    location_lat = tables.Column()
    location_long = tables.Column()
    location_city = tables.Column()
    location_country = tables.Column()
    time_accepted = tables.Column()
    last_updated = tables.Column()
    token = tables.Column()
    active = tables.BooleanColumn()
    no_plates = tables.Column()
    no_matching_plates = tables.Column()
    trust = tables.Column()

    class Meta:
        attrs = {'class': 'table table-striped'}

class table_plates(tables.Table):
    timestamp = tables.Column()
    plate = tables.Column()
    location_lat = tables.Column()
    location_long = tables.Column()
    confidence = tables.Column()
    img_path = tables.LinkColumn(viewname='alpr', args=[A('img_path')])
    processed_violation = tables.BooleanColumn()
    sent = tables.BooleanColumn()

    class Meta:
        attrs = {'class': 'table table-striped'}

class table_violations(tables.Table):
    p1 = tables.Column()
    p2 = tables.Column()
    average_speed = tables.Column()
    unit = tables.Column()
    method = tables.Column()
    time1 = tables.Column()
    time2 = tables.Column()
    distance = tables.Column()
    user_sent_to_peers = tables.BooleanColumn()

    class Meta:
        attrs = {'class': 'table table-striped'}