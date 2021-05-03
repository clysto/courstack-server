from math import ceil

from sqlalchemy.orm import Session

from app.core.models import Course
from app.exceptions import CourseNotFoundException, NotCourseOwnerException


def mkpage(query, schema, page, page_size):
    last_page = ceil(query.count() / page_size)
    return {
        "last_page": last_page,
        "current_page": page,
        "page_size": page_size,
        "contents": schema.dump(
            query[(page - 1) * page_size : page * page_size], many=True
        ),
    }


def course_or_exception(session: Session, course_id, teacher_id):
    course = session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundException(course_id)
    if course.teacher_id != teacher_id:
        raise NotCourseOwnerException
    return course
