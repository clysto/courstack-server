from sqlalchemy.orm import Session, joinedload
from starlette.responses import JSONResponse

from app.decorators import body, db, query, with_user
from app.util import mkpage

from .models import Course
from .schemas import course_schema


@db()
@query("int:page", "int:page_size")
def get_all_courses(db_session: Session, page=1, page_size=10, **kwargs):
    courses = db_session.query(Course).options(joinedload(Course.teacher))
    return JSONResponse(mkpage(courses, course_schema, page, page_size))


@with_user(teacher=True)
@body("course", course_schema)
@db()
def create_course(user, db_session: Session, course, **kwargs):
    course.teacher_id = user.id
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return JSONResponse(course_schema.dump(course))
