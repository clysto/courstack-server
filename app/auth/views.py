import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse

from app.conf import settings
from app.decorators import body, db, query, with_user
from app.exceptions import (
    PasswordIncorrectException,
    UserExistException,
    UserNotExistException,
)
from app.util import mkpage

from .models import User
from .schemas import UserSchema, student_schema, teacher_schema, user_schema

JWT_SECRET = settings.JWT_SECRET


@body("login_user", UserSchema(only=("username", "password")))
@db()
def login(login_user, db_session: Session, **kwargs):
    user = (
        db_session.query(User).filter(User.username == login_user["username"]).first()
    )

    if user is None:
        raise UserNotExistException

    if user.password == login_user["password"]:
        token = jwt.encode(
            {"username": user.username, "user_type": user.user_type, "id": user.id},
            JWT_SECRET,
        )
        return JSONResponse({"message": "登录成功", "access_token": token})
    else:
        raise PasswordIncorrectException


@body("teacher", teacher_schema)
@db()
def teacher_signup(teacher, db_session: Session, **kwargs):
    db_session.add(teacher)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        raise UserExistException
    return JSONResponse(user_schema.dump(teacher))


@body("student", student_schema)
@db()
def student_signup(student, db_session: Session, **kwargs):
    db_session.add(student)
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        raise UserExistException
    return JSONResponse(user_schema.dump(student))


@with_user(detail=True)
def get_current_user(user):
    return JSONResponse(user_schema.dump(user))


@db()
@query("int:page", "int:page_size")
def get_all_users(db_session: Session, page=1, page_size=10, **kwargs):
    users = db_session.query(User)
    return JSONResponse(mkpage(users, user_schema, page, page_size))
