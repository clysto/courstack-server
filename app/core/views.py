from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from starlette.responses import FileResponse, JSONResponse, Response

from app.auth.models import Teacher
from app.conf import settings
from app.decorators import body, db, path_param, query, with_user
from app.exceptions import (
    CourseNotFoundException,
    NotCourseOwnerException,
    SignInTaskExpiredException,
    SignInTaskNotFoundException,
)
from app.util import course_or_exception, mkpage

from .models import (
    Course,
    CourseSection,
    File,
    SignInTask,
    SignInTaskRecord,
    StudentCourseRecord,
)
from .schemas import (
    course_schema,
    course_section_schema,
    file_schema,
    sign_in_task_schema,
)

UPLOAD_FOLDER = settings.UPLOAD_FOLDER


@db()
@query("int:page", "int:page_size", "teacher")
def get_all_courses(db_session: Session, page=1, page_size=10, teacher=None, **kwargs):
    courses = db_session.query(Course).options(joinedload(Course.teacher))
    if teacher is not None:
        courses = courses.join(Teacher).filter(Teacher.username == teacher)
    return JSONResponse(mkpage(courses, course_schema, page, page_size))


@db()
@with_user(student=True)
@query("int:page", "int:page_size")
def get_student_courses(user, db_session: Session, page=1, page_size=10, **kwargs):
    """
    学生选课列表
    """
    courses = (
        db_session.query(Course)
        .join(StudentCourseRecord)
        .filter(StudentCourseRecord.student_id == user.id)
    )
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
@path_param()
@with_user(student=True)
def select_course(course_id, user, db_session: Session, **kwargs):
    """
    学生选课
    """
    course = course_or_exception(db_session, course_id)
    record_exists = (
        db_session.query(StudentCourseRecord)
        .filter(
            StudentCourseRecord.course_id == course_id,
            StudentCourseRecord.student_id == user.id,
        )
        .first()
    )
    if record_exists is None:
        record = StudentCourseRecord(student_id=user.id, course_id=course.id)
        db_session.add(record)
        db_session.commit()
    return JSONResponse({"message": "选课成功"})


@db()
@query("int:page", "int:page_size")
def get_course_sections(db_session: Session, request, page=1, page_size=10, **kwargs):
    course_id = request.path_params["course_id"]
    sections = db_session.query(CourseSection).filter(
        CourseSection.course_id == course_id
    )
    return JSONResponse(mkpage(sections, course_section_schema, page, page_size))


@db()
@body("course_section", course_section_schema)
@with_user(teacher=True)
def create_course_section(db_session: Session, course_section, request, user, **kwargs):
    """
    创建课程卡片
    """
    course_id = request.path_params["course_id"]
    course = db_session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundException(course_id)
    if course.teacher_id != user.id:
        raise NotCourseOwnerException

    # TODO:检查上传的文件是否存在

    course_section.course_id = course_id
    db_session.add(course_section)
    db_session.commit()
    db_session.refresh(course_section)
    return JSONResponse(course_section_schema.dump(course_section))


@db()
async def upload_file(request, db_session: Session):
    """
    文件上传
    """
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
    """
    文件下载
    """
    file_id = request.path_params["file_id"]
    file = db_session.query(File).filter(File.id == file_id).first()
    if file is None:
        return Response(status_code=404)
    return FileResponse(UPLOAD_FOLDER / str(file.id), filename=file.filename)


@db()
@body("sign_in_task", sign_in_task_schema)
@with_user(teacher=True)
def create_sign_in_task(db_session: Session, sign_in_task, user, request):
    course_id = request.path_params["course_id"]
    course = course_or_exception(db_session, course_id, user.id)
    sign_in_task.course_id = course.id
    db_session.add(sign_in_task)
    db_session.commit()
    db_session.refresh(sign_in_task)
    return JSONResponse(sign_in_task_schema.dump(sign_in_task))


@db()
@path_param()
@query("int:page", "int:page_size")
def get_sign_in_task(db_session: Session, course_id, page=1, page_size=10, **kwargs):
    tasks = db_session.query(SignInTask).filter(SignInTask.course_id == course_id)
    return JSONResponse(mkpage(tasks, sign_in_task_schema, page, page_size))


@db()
@path_param()
@with_user(student=True)
def course_sign_in(sign_in_task_id, db_session: Session, user, **kwargs):
    task: SignInTask = (
        db_session.query(SignInTask).filter(SignInTask.id == sign_in_task_id).first()
    )
    if task is None:
        raise SignInTaskNotFoundException(sign_in_task_id)
    if task.time_end < datetime.now():
        raise SignInTaskExpiredException

    # TODO: 检查该学生是否选了该课程
    record = SignInTaskRecord(task_id=sign_in_task_id, student_id=user.id)
    db_session.add(record)
    db_session.commit()
    return JSONResponse({"message": "签到成功"})
