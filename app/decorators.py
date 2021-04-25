from functools import wraps
from inspect import iscoroutinefunction
from json.decoder import JSONDecodeError

from marshmallow.exceptions import ValidationError
from starlette.exceptions import HTTPException

from app.db import Session

from .exceptions import BodyValidationException


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
                return await func(request=request, **{name: data})
            else:
                return func(request=request, **{name: data}, **kwargs)

        return wrapper

    return decorator


def db():
    def decorator(func):
        session = Session()

        @wraps(func)
        async def wrapper(*args, **kwargs):

            if iscoroutinefunction(func):
                return await func(db_session=session, **kwargs)
            else:
                return func(db_session=session, **kwargs)

        return wrapper

    return decorator
