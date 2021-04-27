from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String)
    user_type = Column(String)

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": user_type}


class Student(User):
    __tablename__ = "student"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Teacher(User):
    __tablename__ = "teacher"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    courses = relationship("Course", back_populates="teacher")

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }
