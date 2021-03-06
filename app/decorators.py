import re
from functools import wraps
from inspect import iscoroutinefunction
from json.decoder import JSONDecodeError

from marshmallow.exceptions import ValidationError
from starlette.exceptions import HTTPException

from app.db import Session

from .auth.models import User
from .exceptions import BodyValidationException, UnauthorizedException


def body(name, schema):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, **kwargs):
            try:
                data = schema.load(await request.json())
            except JSONDecodeError as exc:
                raise HTTPException(400, repr(exc))
            except ValidationError as exc:
                raise BodyValidationException(exc)

            if iscoroutinefunction(func):
                return await func(request=request, **{name: data}, **kwargs)
            else:
                return func(request=request, **{name: data}, **kwargs)

        return wrapper

    return decorator


def db():
    def decorator(func):
        session = Session()

        @wraps(func)
        async def wrapper(request, **kwargs):

            if iscoroutinefunction(func):
                response = await func(request=request, db_session=session, **kwargs)
            else:
                response = func(request=request, db_session=session, **kwargs)
            return response

        return wrapper

    return decorator


def with_user(detail=False, teacher=False, student=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, **kwargs):

            user = request.user

            if (
                user.is_authenticated
                and (teacher is False or user.is_teacher == teacher)
                and (student is False or user.is_student == student)
            ):
                if detail:
                    user = (
                        Session.query(User).filter(User.username == user.username).one()
                    )

                if iscoroutinefunction(func):
                    return await func(request=request, user=user, **kwargs)
                else:
                    return func(request=request, user=user, **kwargs)
            else:
                raise UnauthorizedException

        return wrapper

    return decorator


def query(*args):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, **kwargs):
            query_params = {}

            for key in args:
                matched = re.match(r"(int):(.+)", key)
                if matched:
                    key = matched[2]
                if key in request.query_params:
                    if matched and request.query_params[key].isdecimal():
                        query_params[key] = int(request.query_params[key])
                    elif not matched:
                        query_params[key] = request.query_params[key]

            if iscoroutinefunction(func):
                return await func(request=request, **query_params, **kwargs)
            else:
                return func(request=request, **query_params, **kwargs)

        return wrapper

    return decorator


def path_param():
    def decorator(func):
        @wraps(func)
        async def wrapper(request, **kwargs):

            if iscoroutinefunction(func):
                return await func(request=request, **request.path_params, **kwargs)
            else:
                return func(request=request, **request.path_params, **kwargs)

        return wrapper

    return decorator
