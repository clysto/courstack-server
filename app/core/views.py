from datetime import datetime, timedelta
from os.path import isfile
from shutil import copyfileobj
from uuid import uuid4

from qiniu import RtcServer, get_room_token
from qiniu.auth import QiniuMacAuth
from sqlalchemy import desc, extract
from sqlalchemy.orm import Session, joinedload
from starlette.responses import FileResponse, JSONResponse, Response

from app.auth.models import Student, Teacher
from app.conf import settings
from app.decorators import body, db, path_param, query, with_user
from app.exceptions import (
    CourseNotFoundException,
    CourseSectionNotFound,
    NotCourseOwnerException,
    SignInTaskExpiredException,
    SignInTaskNotFoundException,
)
from app.utils import course_or_exception, mkpage, secure_filename

from ..auth.schemas import student_schema
from .models import (
    Course,
    CourseSection,
    SignInTask,
    SignInTaskRecord,
    StudentCourseRecord,
)
from .schemas import course_schema, course_section_schema, sign_in_task_schema

UPLOAD_FOLDER = settings.UPLOAD_FOLDER
QINIU_AK = settings.QINIU_AK
QINIU_SK = settings.QINIU_SK
QINIU_RTC_APPID = settings.QINIU_RTC_APPID


@db()
@query("int:page", "int:page_size", "teacher")
def get_all_courses(db_session: Session, page=1, page_size=10, teacher=None, **kwargs):
    courses = db_session.query(Course).options(joinedload(Course.teacher))
    if teacher is not None:
        courses = courses.join(Teacher).filter(Teacher.username == teacher)
    return JSONResponse(mkpage(courses, course_schema, page, page_size))


@db()
@path_param()
def get_course_detail(course_id, db_session, **kwargs):
    course = db_session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundException(course_id)
    return JSONResponse(course_schema.dump(course))


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
@query("int:year", "int:month")
def get_course_sections(db_session: Session, request, year=None, month=None, **kwargs):
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    course_id = request.path_params["course_id"]
    sections = (
        db_session.query(CourseSection)
        .filter(
            CourseSection.course_id == course_id,
            extract("year", CourseSection.date) == year,
            extract("month", CourseSection.date) == month,
        )
        .order_by(CourseSection.date)
    )
    return JSONResponse(course_section_schema.dump(sections, many=True))


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

    course_section.course_id = course_id
    if len(course_section.attachments) > 0:
        db_session.add(*course_section.attachments)
    db_session.add(course_section)
    db_session.commit()
    db_session.refresh(course_section)
    return JSONResponse(course_section_schema.dump(course_section))


@db()
@with_user(teacher=True)
def delete_course_section(request, user, db_session: Session, **kwargs):
    course_section_id = request.path_params["course_section_id"]
    result = (
        db_session.query(CourseSection, Course)
        .filter(
            CourseSection.id == course_section_id, CourseSection.course_id == Course.id
        )
        .first()
    )
    if result is None:
        raise CourseSectionNotFound(course_section_id)
    (course_section, course) = result
    if course.teacher_id != user.id:
        raise NotCourseOwnerException
    db_session.delete(course_section)
    db_session.commit()
    return JSONResponse({"message": "删除成功"})


@db()
async def upload_file(request, db_session: Session):
    """
    文件上传
    """
    form = await request.form()
    original_filename = form["file"].filename
    filename = "%s.%s" % (uuid4(), secure_filename(original_filename))

    with open(UPLOAD_FOLDER / filename, "wb") as buf:
        copyfileobj(form["file"].file, buf)

    return JSONResponse({"filename": filename})


@query("save")
async def download_file(request, save=None):
    """
    文件下载
    """
    filename = request.path_params["filename"]
    if not isfile(UPLOAD_FOLDER / filename):
        return Response(status_code=404)
    if save is None:
        save = filename

    return FileResponse(UPLOAD_FOLDER / filename, filename=save)


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
@with_user(detail=True)
def get_sign_in_task(
    db_session: Session, user, course_id, page=1, page_size=10, **kwargs
):
    tasks = (
        db_session.query(SignInTask)
        .filter(SignInTask.course_id == course_id)
        .order_by(desc(SignInTask.time_end))
    )
    return JSONResponse(sign_in_task_schema.dump(tasks, many=True))


@db()
def delete_sign_in_task(db_session: Session, **kwargs):
    return JSONResponse()


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

    # 检查是否已经签过到
    exist = (
        db_session.query(SignInTaskRecord)
        .filter(
            SignInTaskRecord.student_id == user.id,
            SignInTaskRecord.task_id == sign_in_task_id,
        )
        .first()
    )

    if exist:
        return JSONResponse({"message": "已经签到成功"})

    record = SignInTaskRecord(task_id=sign_in_task_id, student_id=user.id)
    db_session.add(record)
    db_session.commit()
    return JSONResponse({"message": "签到成功"})


@with_user()
def get_rtc_token(user, request, **kwargs):
    course_id = request.path_params["course_id"]
    # 一天后过期
    expire_at = datetime.now() + timedelta(days=1)
    token = get_room_token(
        QINIU_AK,
        QINIU_SK,
        {
            "appId": QINIU_RTC_APPID,
            "roomName": "room-" + str(course_id),
            "userId": "user-" + str(user.id),
            "expireAt": int(expire_at.timestamp()),
            "permission": "user",
        },
    )
    return JSONResponse({"room_token": token})


@with_user(teacher=True)
@db()
def get_course_students(request, db_session: Session, **kwargs):
    course_id = request.path_params["course_id"]
    students = (
        db_session.query(Student)
        .join(StudentCourseRecord)
        .filter(StudentCourseRecord.course_id == course_id)
        .all()
    )
    return JSONResponse(student_schema.dump(students, many=True))


@db()
@with_user()
def get_sign_in_students(request, db_session: Session, **kwargs):
    sign_in_task_id = request.path_params["sign_in_task_id"]
    students = (
        db_session.query(Student)
        .join(SignInTaskRecord)
        .filter(SignInTaskRecord.task_id == sign_in_task_id)
        .all()
    )
    return JSONResponse(student_schema.dump(students, many=True))


def get_active_rooms(request, **kwargs):
    room_name_prefix = request.path_params["room_name_prefix"]
    server = RtcServer(QiniuMacAuth(QINIU_AK, QINIU_SK))
    info = server.list_active_rooms(QINIU_RTC_APPID, room_name_prefix)
    return JSONResponse(info[0]["rooms"])
