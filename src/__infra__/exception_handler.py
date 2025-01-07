from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response


def request_validation_error_handler(
        request: Request, exception: Exception
) -> Response:
    if not isinstance(exception, RequestValidationError):
        raise Exception(
            f"Exception handler for ValidationException only. ERROR: {exception}"
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exception.errors()},
    )


# Add business here when we want to custom exception message
def exception_handler(request: Request, exception: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exception)},
    )
