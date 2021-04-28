from uuid import uuid4

from sqlalchemy import ARRAY, Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
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


class CourseSection(Base):
    __tablename__ = "course_section"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    title = Column(String)
    content = Column(String)
    date = Column(Date)
    attachments = Column(ARRAY(String, dimensions=1))


class File(Base):
    __tablename__ = "file"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    filename = Column(String)
