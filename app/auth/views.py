from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse

from app.decorators import body, db
from app.exceptions import APIException

from .models import User
from .schemas import UserSchema, teacher_schema, user_schema


@body("login_user", UserSchema(only=("username", "password")))
@db()
def teacher_login(login_user, db_session: Session, **kwargs):
    user = db_session.query(User).filter(User.username == login_user["username"]).one()
    print(user)
    return JSONResponse(user_schema.dump(user))


@body("teacher", teacher_schema)
@db()
async def teacher_signup(teacher, db_session: Session, **kwargs):
    try:
        db_session.add(teacher)
        db_session.commit()
    except IntegrityError:
        db_session.close()
        raise APIException("该用户已经存在")
    db_session.close()
    return JSONResponse(user_schema.dump(teacher))
