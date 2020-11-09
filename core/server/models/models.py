import base64

from django.db import models
from django.utils.functional import cached_property

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
    SHIFT_START = 'shift_start'
    SHIFT_END = 'shift_end'
    INCIDENT = 'incident'
    CHOICES = (
        (SHIFT_START, 'Shift Start'),
        (SHIFT_END, 'Shift End'),
        (INCIDENT, 'Incident'),
    )


class Organization(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title} ({self.id})'


class Worker(models.Model):
    sex = models.CharField(max_length=10, choices=Sex.CHOICES, default=Sex.MALE)
    fio = models.TextField()
    occupation = models.TextField()

    def __str__(self):
        return self.fio


class Site(models.Model):
    # Owner
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, related_name='sites', null=True
    )
    # Description
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True)
    # Geometry
    layout = models.JSONField(null=True, validators=[validate_site_layout])
    corners = models.JSONField(null=True)  # TODO: validators
    # Configuration
    config = models.JSONField(null=True, validators=[validate_site_config])

    @cached_property
    def start_events(self):
        return self.site_events.filter(event_type=EventType.SHIFT_START)

    @cached_property
    def finish_events(self):
        return self.site_events.filter(event_type=EventType.SHIFT_END)

    @cached_property
    def current_workers(self):
        return self.start_events.count() - self.finish_events.count()

    def __str__(self):
        return f'{self.title} ({self.id})'


class Sensor(models.Model):
    # on device uids are coded with `base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')`
    uid = models.UUIDField(unique=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, related_name='sensors', null=True)

    @staticmethod
    def shorten_uuid(uuid):
        return base64.urlsafe_b64encode(uuid.bytes).rstrip(b'=').decode('ascii')

    @cached_property
    def short_uid(self):
        return self.shorten_uuid(self.uid)

    def __str__(self):
        return f'{self.short_uid} at ({self.site.title})'


class SensorReport(models.Model):
    uid = models.UUIDField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='sensor_reports')
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)

    @cached_property
    def short_uid(self):
        return Sensor.shorten_uuid(self.uid)

    def __str__(self):
        return f'{self.short_uid} at ({self.site.title})'


class Shift(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='shifts')
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    time_point = models.DateTimeField()
    data = models.JSONField(null=True)

    def save(self, *args, **kwargs):
        delta = self.finished_at - self.started_at
        self.time_point = self.started_at + delta / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.started_at} at ({self.site.title})'


class SiteEvent(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_events', null=True)
    event_type = models.CharField(max_length=20, choices=EventType.CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    data = models.JSONField(validators=[validate_site_event_data], null=True)

    def __str__(self):
        return f'({self.id}) {self.event_type}'
