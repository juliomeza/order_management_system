from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
import logging
from django.conf import settings

logger = logging.getLogger('custom_logger')

class CustomAPIException(APIException):
    """
    Base class for custom API exceptions.
    Allows defining a reusable error code.
    """
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.error_code = code

class BusinessLogicError(CustomAPIException):
    """
    Exception for business logic errors.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic error'
    default_code = 'business_logic_error'

def custom_exception_handler(exc, context):
    """
    Global exception handler for Django REST Framework (DRF).
    Captures both custom API exceptions and unexpected errors.
    """
    response = exception_handler(exc, context)

    # If DRF does not handle the error, treat it as a 500 internal server error.
    if response is None:
        logger.critical(f"Unhandled error: {str(exc)}", exc_info=True, extra={
            'view': context['view'].__class__.__name__ if 'view' in context else 'Unknown',
            'path': context['request'].path if 'request' in context else 'Unknown'
        })

        return Response({
            'success': False,
            'error': 'Internal server error',
            'detail': str(exc) if settings.DEBUG else 'An unexpected error occurred. Please contact support.',
            'error_code': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # If it's a custom API exception, structure the response.
    if isinstance(exc, CustomAPIException):
        response.data = {
            'success': False,
            'error': response.data.get('detail', str(exc)),
            'error_code': exc.error_code or 'custom_error',
            'detail': response.data
        }

    # Log errors differently based on the status code.
    log_level = logging.ERROR if response.status_code >= 500 else logging.WARNING
    logger.log(log_level, f"API Error: {response.data}", extra={
        'status_code': response.status_code,
        'view': context['view'].__class__.__name__,
        'path': context['request'].path
    })

    return response
