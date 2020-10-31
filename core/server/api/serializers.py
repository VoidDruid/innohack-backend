from enum import Enum

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.models.validators import validate_site_event_data
from server.models import SiteEvent, EventType


def validate_enum(enum):
    def validator(value):
        try:
            if issubclass(enum, Enum):
                enum(value)
            else:
                if value not in enum.__dict__.values():
                    raise ValueError
        except ValueError:
            raise ValidationError('Wrong enum value')

    return validator


class SiteEventSerializer(serializers.Serializer):
    event_type = serializers.CharField(max_length=20, validators=[validate_enum(EventType)])
    created_at = serializers.DateTimeField()
    data = serializers.JSONField(validators=[validate_site_event_data], allow_null=True)

    def create(self, validated_data):
        return SiteEvent.objects.create(**validated_data)

class SiteSerializer(serializers.Serializer):

    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, related_name='sites', null=True
    )
    # Description
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True)
    # Geometry
    layout = models.JSONField(null=True, validators=[validate_site_layout])
    long = models.FloatField()
    lat = models.FloatField()
    # Configuration
    config = models.JSONField(null=True, validators=[validate_site_config])

    event_type = serializers.CharField(max_length=20, validators=[validate_enum(EventType)])
    created_at = serializers.DateTimeField()
    data = serializers.JSONField(validators=[validate_site_event_data], allow_null=True)

    def create(self, validated_data):
        return SiteEvent.objects.create(**validated_data)

