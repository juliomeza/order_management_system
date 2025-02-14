from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from apps.core.models import Status
import logging

logger = logging.getLogger('custom_logger')

def validate_lookup_code(value):
    """
    Validator for lookup_code fields that ensures:
    - At least 2 characters
    - Only contains alphanumeric chars, underscores, and hyphens
    - No spaces or special characters allowed
    """
    # Verificar longitud mínima
    if len(value) < 2:
        logger.warning(f"Validation failed: lookup_code '{value}' is too short.")
        raise ValidationError(
            _('Lookup code must be at least 2 characters long.'),
            code='min_length')
    
    # Verificar caracteres permitidos
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', value):
        logger.warning(f"Validation failed: lookup_code '{value}' contains invalid characters.")
        raise ValidationError(
            _('Lookup code can only contain letters, numbers, underscores, and hyphens.'),
            code='invalid_lookup_code')

class StatusValidator:
    """
    General validator for status types.
    Validates that the status matches the expected status type for the model.
    """
    def __init__(self, expected_status_type):
        self.expected_status_type = expected_status_type

    def __call__(self, status_id):
        """
        Validate the status type.
        :param status_id: The ID or instance of the Status model.
        """
        if not status_id:
            logger.warning("Validation failed: Status ID is missing or null.")
            raise ValidationError(
                _('Status cannot be null or empty.'),
                code='missing_status'
            )

        # Si es un número entero (ID), obtener la instancia de Status
        if isinstance(status_id, int):
            try:
                status = Status.objects.get(pk=status_id)
            except Status.DoesNotExist:
                logger.error(f"Validation failed: Status ID {status_id} does not exist.")
                raise ValidationError(
                    _('Invalid status. No matching status found.'),
                    code='invalid_status'
                )
        else:
            status = status_id

        # Validar que el status_type coincida con el esperado
        if status.status_type != self.expected_status_type:
            logger.warning(f"Validation failed: Expected status_type '{self.expected_status_type}', but got '{status.status_type}'.")
            raise ValidationError(
                _('Invalid status type. Expected %(expected)s but got %(got)s.'),
                code='invalid_status_type',
                params={
                    'expected': self.expected_status_type,
                    'got': status.status_type
                }
            )

class TimestampValidator:
    """
    Validates timestamp logical consistency in TimeStampedModel.
    Ensures modified_date is after created_date.
    """
    def __call__(self, model_instance):
        if (model_instance.modified_date and 
            model_instance.created_date and
            model_instance.modified_date < model_instance.created_date):
            logger.error(
                f"Validation failed: modified_date ({model_instance.modified_date}) "
                f"is before created_date ({model_instance.created_date})."
            )
            raise ValidationError(
                _('Modified date cannot be before created date'),
                code='invalid_timestamp_order'
            )