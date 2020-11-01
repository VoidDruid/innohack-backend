from enum import Enum

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.models import SensorReport, Site, SiteEvent, Worker


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


class SiteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteEvent
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'


class SiteShortSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    id = serializers.IntegerField()


class SensorReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReport
        fields = '__all__'
