from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="courses")
    date_start = Column(Date)
    date_end = Column(Date)
    cover = Column(String)


class StudentCourseRecord(Base):
    __tablename__ = "student_course_record"

    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)


class CourseSection(Base):
    __tablename__ = "course_section"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    title = Column(String)
    content = Column(String)
    date = Column(Date)
    attachments = relationship("Attachment")


class Attachment(Base):
    __tablename__ = "attachment"
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("course_section.id"))
    original_filename = Column(String)
    filename = Column(String)


class SignInTask(Base):
    """
    签到任务
    """

    __tablename__ = "sign_in_task"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    course_id = Column(Integer, ForeignKey("course.id"))


class SignInTaskRecord(Base):
    """
    签到记录
    """

    __tablename__ = "sign_in_task_record"
    task_id = Column(Integer, ForeignKey("sign_in_task.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
