from sqlalchemy.orm import Session, joinedload
from starlette.responses import FileResponse, JSONResponse, Response

from app.conf import settings
from app.decorators import body, db, query, with_user
from app.util import mkpage

from .models import Course, CourseSection, File
from .schemas import course_schema, course_section_schema, file_schema

UPLOAD_FOLDER = settings.UPLOAD_FOLDER


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


@db()
@query("int:page", "int:page_size")
def get_course_sections(db_session: Session, request, page=1, page_size=10, **kwargs):
    course_id = request.path_params["course_id"]
    sections = db_session.query(CourseSection).filter(
        CourseSection.course_id == course_id
    )
    return JSONResponse(mkpage(sections, course_section_schema, page, page_size))


@db()
async def upload_file(request, db_session: Session):
    file = File()
    form = await request.form()
    filename = form["file"].filename
    file.filename = filename
    db_session.add(file)
    db_session.commit()
    db_session.refresh(file)
    with open(UPLOAD_FOLDER / str(file.id), "wb") as f:
        f.write(await form["file"].read())
    return JSONResponse(file_schema.dump(file))


@db()
async def download_file(request, db_session: Session):
    file_id = request.path_params["file_id"]
    file = db_session.query(File).filter(File.id == file_id).first()
    if file is None:
        return Response(status_code=404)
    return FileResponse(UPLOAD_FOLDER / str(file.id), filename=file.filename)
