import uuid

from django.contrib.postgres import fields as pg
from django.db import models

from .validators import (
    validate_sensor_report_data,
    validate_site_config,
    validate_site_event_data,
    validate_site_layout,
)


class Sex:
    MALE = 'M'
    FEMALE = 'F'
    CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )


class EventType:
    SHIFT_START = 'ss'
    SHIFT_END = 'se'
    INCIDENT = 'i'
    CHOICES = (
        (SHIFT_START, 'Shift Start'),
        (SHIFT_END, 'Shift End'),
        (INCIDENT, 'Incident'),
    )


class Organization(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)


class Worker(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    sex = models.CharField(max_length=10, choices=Sex.CHOICES, default=Sex.MALE)
    fio = models.TextField()
    occupation = models.TextField()


class Site(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # Owner
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


class Sensor(models.Model):
    # on device uids are coded with `base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')`
    uid = models.UUIDField(unique=True, editable=False)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, related_name='sensors', null=True)


class SensorReport(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, related_name='reports', null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='sensor_reports')
    data = models.JSONField(validators=[validate_sensor_report_data])
    created_at = models.DateTimeField(auto_now=True)


class Shift(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='shifts')
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()


class SiteEvent(models.Model):
    event_type = models.CharField(max_length=20, choices=EventType.CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    data = models.JSONField(validators=[validate_site_event_data], null=True)


class ShiftReport(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='shift_reports')
