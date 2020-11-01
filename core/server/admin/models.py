import base64

from django.contrib import admin

from server.models import Worker, Site, Organization, Sensor, SensorReport, Shift, SiteEvent, ShiftReport


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

    def short_uid(self, obj):
        return base64.urlsafe_b64encode(obj.uid.bytes).rstrip(b'=').decode('ascii')


@admin.register(SensorReport)
class SensorReportAdmin(SensorAdmin):
    list_display = ('created_at', 'site_title', 'uid', 'short_uid')


@admin.register(Shift)
class ShiftAdmin(SiteBound):
    list_display = ('started_at', 'finished_at', 'site_title')
    search_fields = ('site__title',)
    list_filter = ('site__title',)  # TODO: titles not unique


@admin.register(ShiftReport)
class ShiftReportAdmin(SiteBound):
    list_display = ('site_title',)
    search_fields = ('site__title',)
    list_filter = ('site__title',)  # TODO: titles not unique


@admin.register(SiteEvent)
class SiteEventAdmin(SiteBound):
    list_display = ('event_type', 'site_title', 'created_at')
    search_fields = ('site__title', 'data')
    list_filter = ('site__title', 'event_type')  # TODO: titles not unique


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('organization_title', 'id', 'title')
    list_filter = ('organization__title',)
    search_fields = ('organization__title', 'title')

    list_select_related = ('organization',)

    def organization_title(self, obj):
        if obj.organization is not None:
            return obj.organization.title
        return None
    organization_title.admin_order_field = 'organization__title'
    organization_title.short_description = 'Застройщик'

