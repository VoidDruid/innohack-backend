from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand, CommandError

from server.models import Shift, Site, Worker, SensorReport, SiteEvent, EventType


class Command(BaseCommand):
    help = 'Build missing shift reports'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=lambda s: datetime.strptime(s, '%d.%m.%Y').date())

    @staticmethod
    def make_shift_boundaries(date):
        return (
            (datetime.combine(date, time(hour=7)), datetime.combine(date, time(hour=15))),
            (datetime.combine(date, time(hour=15)), datetime.combine(date, time(hour=23))),
            (datetime.combine(date, time(hour=23)), datetime.combine(date+timedelta(days=1), time(hour=7))),
        )

    @staticmethod
    def daterange(start, end):
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()

        current = start
        while current < end:
            yield current
            current = current + timedelta(days=1)

    @staticmethod
    def create_report_in_boundaries(site, start, end):
        events = SiteEvent.objects.filter(created_at__range=(start, end)).all()
        sensor_reports = SensorReport.objects.filter(created_at__range=(start, end)).all()

        incidents = 0
        workers = 0

        for event in events:
            if event.event_type == EventType.INCIDENT:
                incidents += 1
            # following logic is INCORRECT and is a hack for hackathon - should be rewritten!
            elif event.event_type == EventType.SHIFT_START:
                workers += 1
            elif event.event_type == EventType.SHIFT_END:
                workers -= 1

        sensor_averages = {}
        for report in sensor_reports:
            sensor_data = sensor_averages.get(report.uid, {})
            for metric in report.data:
                if report.data[metric] in ('nan', 'inf', '-inf'):
                    continue
                values = sensor_data.get(metric, [])
                values.append(report.data[metric])

        for sensor_uid in sensor_averages:
            sensor_data = sensor_averages[sensor_uid]
            for metric, values in sensor_data.items():
                count = len(values)
                average = sum(map(float, values)) / count
                sensor_data[metric] = average

        data = {
            'workers': workers,
            'incidents': incidents,
            'sensor_data': sensor_averages,
        }
        shift = Shift(started_at=start, finished_at=end, site=site, data=data)
        shift.save()
        return True

    def handle(self, *args, **options):
        start_date = options['start_date']
        created_reports = 0

        self.stdout.write('Starting processing')

        for date in self.daterange(start_date, datetime.now() + timedelta(days=1)):
            for boundaries in self.make_shift_boundaries(date):
                self.stdout.write(f'Building for {boundaries}')
                for site in Site.objects.all():
                    is_created = self.create_report_in_boundaries(site, *boundaries)
                    if is_created:
                        created_reports += 1

        self.stdout.write(self.style.SUCCESS(f'Created <{created_reports}> reports'))