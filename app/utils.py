import os
import re
import unicodedata
from math import ceil

from sqlalchemy.orm import Session

from app.core.models import Course
from app.exceptions import CourseNotFoundException, NotCourseOwnerException

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")

_windows_device_files = (
    "CON",
    "AUX",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
    "PRN",
    "NUL",
)


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


def course_or_exception(session: Session, course_id, teacher_id=None):
    course = session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundException(course_id)
    if teacher_id is not None and course.teacher_id != teacher_id:
        raise NotCourseOwnerException
    return course


def secure_filename(filename: str) -> str:
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename
