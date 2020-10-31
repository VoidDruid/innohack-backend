from django.contrib import admin

from server.models import Worker, Site, Organization, Sensor, SensorReport, Shift, SiteEvent, ShiftReport


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorReport)
class SensorReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteEvent)
class SiteEventAdmin(admin.ModelAdmin):
    pass


@admin.register(ShiftReport)
class ShiftReportAdmin(admin.ModelAdmin):
    pass
