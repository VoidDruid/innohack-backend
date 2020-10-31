from django.core.exceptions import ValidationError
from pydantic import ValidationError as PydanticError

from .schemas import SensorReportData, SiteConfig, SiteEventData, SiteLayout


def to_django_error(error):
    if isinstance(error, PydanticError):
        return ValidationError(str(error))  # TODO

    raise RuntimeError('Unknown error')


def wrap_errors(model, value):
    try:
        model.validate(value)
    except Exception as e:
        raise to_django_error(e)


def validate_site_layout(value):
    wrap_errors(SiteLayout, value)


def validate_site_config(value):
    wrap_errors(SiteConfig, value)


def validate_sensor_report_data(value):
    wrap_errors(SensorReportData, value)


def validate_site_event_data(value):
    wrap_errors(SiteEventData, value)
