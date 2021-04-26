from starlette.applications import Starlette
from starlette.authentication import (
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
    AuthCredentials,
)
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from jwt.exceptions import InvalidSignatureError, DecodeError

from .conf import settings
from .exceptions import APIException, BodyValidationException
from .urls import routes
from .views import api_exception, body_validation_exception, http_exception

import jwt

JWT_SECRET = settings.JWT_SECRET


class AuthenticatedUser(BaseUser):
    def __init__(self, username, user_type, user_id):
        self.username = username
        self.user_type = user_type
        self.id = user_id

    @property
    def is_teacher(self) -> str:
        return self.user_type == "teacher"

    @property
    def is_student(self) -> str:
        return self.user_type == "student"

    @property
    def identity(self) -> str:
        return self.id

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return ""


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "bearer":
                return
            decoded = jwt.decode(credentials, JWT_SECRET, "HS256")
        except (InvalidSignatureError, DecodeError):
            return AuthCredentials(["authenticated"]), UnauthenticatedUser()

        return AuthCredentials(["authenticated"]), AuthenticatedUser(
            decoded["username"], decoded["user_type"], decoded["id"]
        )


exception_handlers = {
    HTTPException: http_exception,
    BodyValidationException: body_validation_exception,
    APIException: api_exception,
}

middleware = [Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())]

app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    exception_handlers=exception_handlers,
    middleware=middleware,
)
