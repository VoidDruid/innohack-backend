import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay

from server.models import (
    Organization,
    Sensor,
    SensorReport,
    Shift,
    Site,
    SiteEvent,
    Worker,
)
from .forms import *


class SiteBound(admin.ModelAdmin):
    list_select_related = ('site',)

    def site_title(self, obj):
        if obj.site is not None:
            return obj.site.title
        return None

    site_title.admin_order_field = 'site__title'
    site_title.short_description = 'Площадка'


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'occupation', 'sex')
    list_filter = ('sex',)
    search_fields = ('fio', 'occupation')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Sensor)
class SensorAdmin(SiteBound):
    list_display = ('site_title', 'uid', 'short_uid')
    search_fields = ('site__title', 'uid')
    list_filter = ('site__title',)  # TODO: titles not unique


@admin.register(SensorReport)
class SensorReportAdmin(SiteBound):
    list_display = ('created_at', 'site_title', 'uid', 'short_uid')
    search_fields = ('site__title', 'uid')
    list_filter = ('site__title',)  # TODO: titles not unique


@admin.register(Shift)
class ShiftAdmin(SiteBound):
    list_display = ('started_at', 'finished_at', 'site_title', 'has_report')
    search_fields = ('site__title',)
    list_filter = ('site__title',)  # TODO: titles not unique
    fieldsets = (
        (
            None,
            {
                'fields': ('site',),
            },
        ),
        (
            'Параметры смены',
            {
                'fields': ('started_at', 'finished_at'),
            },
        ),
        (
            'Прочие данные',
            {
                'classes': ('collapse',),
                'fields': ('has_report', 'data', 'time_point'),
            },
        ),
        (
            'Статистика',
            {
                'fields': (),
            },
        ),
    )
    readonly_fields = ('has_report', 'data', 'time_point')

    def has_report(self, obj):
        return bool(obj.data)
    has_report.short_description = 'Отчет готов'


@admin.register(SiteEvent)
class SiteEventAdmin(SiteBound):
    list_display = ('event_type', 'site_title', 'created_at')
    search_fields = ('site__title', 'data')
    list_filter = ('site__title', 'event_type')  # TODO: titles not unique

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            SiteEvent.objects.annotate(date=TruncDay('created_at'))
            .values('date')
            .annotate(y=Count('id'))
            .order_by('-date')
        )

        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {'chart_data': as_json}

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('organization_title', 'id', 'title')
    list_filter = ('organization__title',)
    search_fields = ('organization__title', 'title')

    fieldsets = (
        (
            None,
            {
                'fields': ('organization',),
            },
        ),
        (
            'Описание',
            {
                'fields': ('title', 'description'),
            },
        ),
        (
            'Параметры',
            {
                'classes': ('collapse',),
                'fields': ('layout', 'corners', 'config'),
            },
        ),
        (
            'Статистика',
            {
                'fields': ('current_workers',),
            },
        ),
    )
    readonly_fields = ('current_workers',)

    list_select_related = ('organization',)

    def organization_title(self, obj):
        if obj.organization is not None:
            return obj.organization.title
        return None

    organization_title.admin_order_field = 'organization__title'
    organization_title.short_description = 'Застройщик'
