from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_date_hierarchy(start_date, end_date):
    """
    Validates that start_date comes before end_date.
    Used for any model with date ranges in the Inventory app.
    """
    if start_date and end_date and start_date >= end_date:
        raise ValidationError(
            _('Start date must be before end date'),
            code='invalid_date_range'
        )