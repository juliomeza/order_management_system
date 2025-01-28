from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models import Q
import re

def validate_lookup_code(value):
    """
    Validator for lookup_code fields that ensures:
    - At least 2 characters
    - Only contains alphanumeric chars, underscores, and hyphens
    - No spaces or special characters allowed
    """
    # Verificar longitud mínima
    if len(value) < 2:
        raise ValidationError(
            _('Lookup code must be at least 2 characters long and can only contain letters, numbers, underscores, and hyphens.'),
            code='min_length'
        )
    
    # Verificar caracteres permitidos
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', value):
        raise ValidationError(
            _('Lookup code can only contain letters, numbers, underscores, and hyphens.'),
            code='invalid_lookup_code'
        )

class StatusValidator:
    """
    General validator for status types.
    Validates that the status matches the expected status type for the model.
    """
    def __init__(self, expected_status_type):
        """
        :param expected_status_type: The expected status type for the model.
        """
        self.expected_status_type = expected_status_type

    def __call__(self, status):
        """
        Validate the status type.
        :param status: The status instance to validate.
        """
        if not status:
            raise ValidationError(
                _('Status cannot be null or empty.'),
                code='missing_status'
            )

        if status.status_type != self.expected_status_type:
            raise ValidationError(
                _('Invalid status type. Expected %(expected)s but got %(got)s.'),
                code='invalid_status_type',
                params={
                    'expected': self.expected_status_type,
                    'got': status.status_type
                }
            )

def validate_project_customer_hierarchy(project, customer=None):
    """
    Validates project-customer hierarchy relationships.
    Can be called with just project (to validate its customer)
    or with both project and customer (to validate they match).
    """
    if not project:
        return
        
    if customer and project.customer != customer:
        raise ValidationError(
            _('Project %(project)s does not belong to customer %(customer)s'),
            code='invalid_project_customer',
            params={
                'project': project,
                'customer': customer
            }
        )

def validate_date_hierarchy(start_date, end_date):
    """
    Validates that start_date comes before end_date.
    Used for any model with date ranges.
    """
    if start_date and end_date and start_date > end_date:
        raise ValidationError(
            _('Start date must be before end date'),
            code='invalid_date_range'
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
            raise ValidationError(
                _('Modified date cannot be before created date'),
                code='invalid_timestamp_order'
            )

def validate_user_permissions(user, project):
    """
    Validates user has permissions for the given project.
    Used in save() methods where user context is needed.
    """
    if not user:
        return
        
    if not user.is_superuser:
        if not user.project:
            raise ValidationError(
                _('User must be assigned to a project'),
                code='no_project_assigned'
            )
        if user.project != project:
            raise ValidationError(
                _('User does not have permission for this project'),
                code='invalid_project_permission'
            )