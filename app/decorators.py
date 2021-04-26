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
                response = await func(db_session=session, **kwargs)
            else:
                response = func(db_session=session, **kwargs)
            session.close()
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
                    with Session() as session:
                        user = (
                            session.query(User)
                            .filter(User.username == user.username)
                            .one()
                        )

                if iscoroutinefunction(func):
                    return await func(user=user, **kwargs)
                else:
                    return func(user=user, **kwargs)
            else:
                raise UnauthorizedException

        return wrapper

    return decorator
