from starlette.applications import Starlette
from starlette.exceptions import HTTPException

from .conf import settings
from .exceptions import APIException, BodyValidationException
from .urls import routes
from .views import api_exception, body_validation_exception, http_exception

exception_handlers = {
    HTTPException: http_exception,
    BodyValidationException: body_validation_exception,
    APIException: api_exception,
}

app = Starlette(
    debug=settings.DEBUG, routes=routes, exception_handlers=exception_handlers
)
