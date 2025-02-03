import logging

logger = logging.getLogger('custom_logger')

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            
            if response.status_code >= 400:
                log_level = logging.ERROR if response.status_code >= 500 else logging.WARNING
                logger.log(
                    log_level,
                    f"HTTP {response.status_code} - {request.method} {request.path}",
                    extra={
                        'status_code': response.status_code,
                        'method': request.method,
                        'path': request.path
                    }
                )
            return response
        
        except Exception as e:
            logger.critical(
                f"Unhandled error in middleware: {str(e)}",
                exc_info=True,
                extra={'path': request.path, 'method': request.method}
            )
            raise
