from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.decorators import body, db, with_user

from .models import Course
from .schemas import course_schema


@db()
def get_all_courses(db_session: Session, **kwargs):
    courses = db_session.query(Course).all()
    return JSONResponse(course_schema.dump(courses, many=True))


@with_user(teacher=True)
@body("course", course_schema)
@db()
def create_course(user, db_session: Session, course, **kwargs):
    course.teacher_id = user.id
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return JSONResponse(course_schema.dump(course))
