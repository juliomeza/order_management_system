from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import logging

logger = logging.getLogger('custom_logger')

def validate_expected_delivery_date(order_instance):
    """
    Validator to ensure the expected delivery date is:
    1. Not earlier than the creation date (if exists)
    2. Not earlier than current time
    """
    now = timezone.now()
    
    if order_instance.expected_delivery_date < now:
        logger.error(
            f"Validation failed: expected_delivery_date ({order_instance.expected_delivery_date}) "
            f"is before the current time ({now})."
        )
        raise ValidationError(
            _('Expected delivery date cannot be earlier than current date and time.'),
            code='delivery_date_past'
        )
    
    if order_instance.created_date and order_instance.expected_delivery_date < order_instance.created_date:
        logger.error(
            f"Validation failed: expected_delivery_date ({order_instance.expected_delivery_date}) "
            f"is before order creation date ({order_instance.created_date})."
        )
        raise ValidationError(
            _('Expected delivery date cannot be earlier than the order creation date.'),
            code='invalid_delivery_date'
        )