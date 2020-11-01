from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    SiteEvent = apps.get_model('server', 'SiteEvent')
    db_alias = schema_editor.connection.alias

    for site_event in SiteEvent.objects.using(db_alias).all():
        if site_event.data is not None and 'site_id' in site_event.data:
            site_event.site_id = site_event.data.pop('site_id')
        site_event.save()


def reverse_func(apps, schema_editor):
    SiteEvent = apps.get_model('server', 'SiteEvent')
    db_alias = schema_editor.connection.alias

    for site_event in SiteEvent.objects.using(db_alias).all():
        if site_event.site_id is not None:
            site_event.data['site_id'] = site_event.site_id
        site_event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_auto_20201101_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteevent',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_events', to='server.site'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='uid',
            field=models.UUIDField(unique=True),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
