from enum import Enum

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.models.validators import validate_site_event_data, validate_site_layout, validate_site_config
from server.models import SiteEvent, EventType, Site, Sex, Worker


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
    organization = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=250, allow_null=True)
    layout = serializers.JSONField(allow_null=True, validators=[validate_site_layout])
    long = serializers.FloatField()
    lat = serializers.FloatField()
    config = serializers.JSONField(allow_null=True, validators=[validate_site_config])

    def create(self, validated_data):
        return Site.objects.create(**validated_data)


class WorkerSerializer(serializers.Serializer):
    sex = serializers.CharField(max_length=10, validators=[validate_enum(Sex)], default=Sex.MALE)
    fio = serializers.CharField(max_length=100)
    occupation = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Worker.objects.create(**validated_data)