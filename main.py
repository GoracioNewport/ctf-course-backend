from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Union

import crud
import models
import schemas
import security
from database import engine, get_db
from utils import stringToList

from ppc_tasks import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://backctf.goracionewport.ru",
    "https://backctf.goracionewport.ru",
    "http://shmitctf.goracionewport.ru",
    "https://shmitctf.goracionewport.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token", response_model=security.Token)
async def login_for_access_token(req: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = security.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = {"access_token": access_token, "token_type": "bearer"}
    return response


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, token_user: security.User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/courses", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    courses = crud.get_courses(db)
    return courses


@app.get("/courses/", response_model=List[schemas.Task])
def read_course(path: str, db: Session = Depends(get_db), token_user: security.User = Depends(security.get_current_user)):
    course = crud.get_course_by_path(db, path)
    if not course:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if not course.unlocked:

        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="nope"
        )

    tasks = crud.get_tasks_by_course_id(db, courseId=course.id)
    return tasks


@app.get("/userSolved", response_model=List[int])
def get_solved(db: Session = Depends(get_db), token_user: security.User = Depends(security.get_current_user)):
    user = crud.get_user_by_username(db, token_user.username)

    return stringToList(user.solved)


@app.post("/sendAnswer")
def send_answer(taskAnswer: schemas.taskAnswer, db: Session = Depends(get_db), token_user: security.User = Depends(security.get_current_user)):
    answer = taskAnswer.answer
    taskId = taskAnswer.taskId

    user = crud.get_user_by_username(db, token_user.username)
    solved = stringToList(user.solved)

    task = crud.get_task_by_id(db, taskId)

    if not task:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    course = crud.get_course(db, task.course_id)

    if not course.unlocked:

        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="nope"
        )

    if solved[taskId] == 2:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task already solved"
        )

    if not security.verify_hash(answer, task.hashed_answer):

        crud.mark_task(db, user.id, task.id, 1)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong Answer"
        )

    crud.add_points_to_user(db, user.id, task.course_id, task.weight)
    if not security.check_admin(user.username):
        crud.mark_task(db, user.id, task.id, 2)
        crud.add_task_solution(db, task.id)

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="OK"
    )


@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    courses = crud.get_courses(db)

    userList = list()

    for user in users:
        singleUser = {
            'username': user.username,
            'score': stringToList(user.score)
        }

        userList.append(singleUser)

    courseList = list()

    for course in courses:
        singleCourse = {
            'name': course.name,
            'id': course.id
        }

        if course.unlocked:
            courseList.append(singleCourse)

    response = {
        'courses': courseList,
        'users': userList
    }

    return response


@app.get("/getDocs")
def get_docs(db: Session = Depends(get_db)):
    return crud.get_docs(db)


@app.get("/flag")
def get_flag():
    return {'flag':'gctf_i_knew_it_all_along'}


# --- ADMIN SECTION ---


@app.post("/unlockCourse")
def unlock_course(course_id: int, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    crud.unlock_course(db, course_id)
    return admin


@app.post("/createCourse")
def create_course(course_name: str, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    crud.create_course(db, course_name)
    return admin


@app.post("/createTask")
def create_task(task_name: str, task_description: str, course_id: int, weight: int, answer: str, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    crud.create_task(db, task_name, task_description,
                     course_id, weight, answer)
    return admin


@app.delete("/deleteUser")
def delete_user(username: str, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    crud.delete_user(db, username)
    return admin


@app.delete("/deleteTask")
def delete_task(task_id: int, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    crud.delete_task(db, task_id)
    return admin


@app.post("/updateTask")
def update_task(task_id: int, answer: Union[str, None] = None, name: Union[str, None] = None, description: Union[str, None] = None, course_id: Union[int, None] = None, weight: Union[int, None] = None, solved: Union[int, None] = None, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    crud.update_task(db, task_id, name, description,
                     course_id, weight, answer, solved)
    return admin


@app.post("/createDoc")
def create_doc(name: str, description: str, db: Session = Depends(get_db), admin: bool = Depends(security.is_admin)):
    doc = crud.create_doc(db, name, description)
    return doc

