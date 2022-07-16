from sqlalchemy.orm import Session
from . import models, schemas, security


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_name(db: Session, name: str):
    return db.query(models.Course).filter(models.Course.name == name).first()


def get_course_by_path(db: Session, path: str):
    return db.query(models.Course).filter(models.Course.path == path).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    zeros_string = "[" + ("0," * 99) + "0]"
    db_user = models.User(username=user.username, hashed_password=hashed_password, score=0, solved=zeros_string)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_courses(db: Session):
    return db.query(models.Course).all()


def get_tasks_by_course_id(db: Session, courseId: str):
    return db.query(models.Task).filter(models.Task.course_id == courseId).all()
