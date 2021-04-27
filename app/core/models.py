from sqlalchemy import Column, Date, ForeignKey, Integer, String
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


# class CourseSections(Base):
#     pass
