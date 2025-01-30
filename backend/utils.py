# backend/utils.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response.
    response = exception_handler(exc, context)

    # If the exception is already handled, format it.
    if response is not None:
        response.data = {
            "status_code": response.status_code,
            "error_message": response.data.get("detail", "An error occurred."),
            "errors": response.data if "detail" not in response.data else None,
        }
    else:
        # Handle unexpected errors
        response = Response({
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error_message": "Unexpected error occurred.",
            "errors": str(exc),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
