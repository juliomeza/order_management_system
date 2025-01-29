from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger('custom_logger')

def validate_date_hierarchy(start_date, end_date):
    """
    Validates that start_date comes before end_date.
    Used for any model with date ranges in the Inventory app.
    """
    if start_date and end_date and start_date >= end_date:
        logger.error(
            f"Validation failed: start_date ({start_date}) is not before end_date ({end_date})."
        )
        raise ValidationError(
            _('Start date must be before end date'),
            code='invalid_date_range'
        )

def validate_unique_price_history(material, effective_date, end_date, instance=None):
    """
    Ensures no overlapping price history entries for the same material.
    
    Args:
        material: Material instance
        effective_date: Start date of the price period
        end_date: End date of the price period (can be None)
        instance: Current MaterialPriceHistory instance being validated (if updating)
    """
    if not material or not effective_date:
        logger.warning("Validation skipped: Material or effective_date is missing.")
        return

    # Base query for overlapping prices
    overlapping_query = material.price_history.filter(
        models.Q(end_date__gt=effective_date) | models.Q(end_date__isnull=True),
        effective_date__lt=(end_date or timezone.now())
    )

    # Exclude current instance if updating
    if instance and instance.pk:
        overlapping_query = overlapping_query.exclude(pk=instance.pk)

    if overlapping_query.exists():
        logger.error(
            f"Validation failed: Price range ({effective_date} - {end_date}) "
            f"overlaps with an existing record for material {material.lookup_code}."
        )
        raise ValidationError(
            _('This price range overlaps with an existing record for this material.'),
            code='overlapping_price_range'
        )