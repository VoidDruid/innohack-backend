from functools import wraps

from django.core.exceptions import ValidationError
from pydantic import ValidationError as PydanticError

from .schemas import SensorReportData, SiteConfig, SiteEventData, SiteLayout


def pydantic_validation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except PydanticError as error:
            raise ValidationError(str(error))  # TODO

    return wrapper


def model_validation(model):
    return pydantic_validation(model.validate)


validate_site_layout = model_validation(SiteLayout)
validate_site_config = model_validation(SiteConfig)
validate_sensor_report_data = model_validation(SensorReportData)
validate_site_event_data = model_validation(SiteEventData)
