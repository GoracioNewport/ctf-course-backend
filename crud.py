from sqlalchemy.orm import Session
import models
import schemas
import security
import utils


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


def get_users(db: Session, skip: int = 0, limit: int = 200):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_hash(user.password)
    solved_string = "[" + ("0," * 99) + "0]"
    score_string = "[" + ("0," * 9) + "0]"
    db_user = models.User(username=user.username, hashed_password=hashed_password,
                          score=score_string, solved=solved_string)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_courses(db: Session):
    return db.query(models.Course).all()


def get_tasks_by_course_id(db: Session, courseId: int):
    return db.query(models.Task).filter(models.Task.course_id == courseId).all()


def get_task_by_id(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()


def add_points_to_user(db: Session, user_id: int, course_id: int, points: int):
    user = get_user(db, user_id)

    score = utils.stringToList(user.score)
    score[course_id] += points
    user.score = utils.listToString(score)
    db.commit()


def mark_task(db: Session, user_id: int, task_id: int, status: int):
    user = get_user(db, user_id)

    solved = utils.stringToList(user.solved)
    solved[task_id] = status
    user.solved = utils.listToString(solved)
    db.commit()


def add_task_solution(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    task.solved += 1
    db.commit()


# --- ADMIN SECTION ---

def create_course(db: Session, course_name: str):
    db_course = models.Course(
        name=course_name, description="", path=course_name.lower(), unlocked=0)

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def create_task(db: Session, task_name: str, task_desc: str, course_id: int, weight: int, answer: str):
    hashed_answer = security.get_hash(answer)

    task_db = models.Task(name=task_name, description=task_desc, course_id=course_id,
                          weight=weight, solved=0, hashed_answer=hashed_answer)

    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


def unlock_course(db: Session, course_id: int):
    course = get_course(db, course_id)

    course.unlocked = 1
    db.commit()


def delete_user(db: Session, username: str):
    db.query(models.User).filter(models.User.username == username).delete()

    db.commit()


def delete_task(db: Session, task_id: int):
    db.query(models.Task).filter(models.Task.id == task_id).delete()

    db.commit()


def update_answer(db: Session, task_id: int, answer: str):
    task_db = db.query(models.Task).filter(models.Task.id == task_id).first()

    task_db.hashed_answer = security.get_hash(answer)
    db.commit() 