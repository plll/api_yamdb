from django.core.exceptions import ValidationError
import datetime as dt


def validate_year(value):
    if dt.date.today().year < value and value > 0:
        raise ValidationError(
            'Неправильно указан год'
        )
    return value
