from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    score = Column(Integer)
    solved = Column(String)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    path = Column(String)
    unlocked = Column(Boolean)

    tasks = relationship("Task", back_populates="course")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
    weight = Column(Integer)
    solved = Column(Integer)
    hashed_answer = Column(String)

    course = relationship("Course", back_populates="tasks")


class Doc(Base):
    __tablename__ = "docs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    unlocked = Column(Boolean)
