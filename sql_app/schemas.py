from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    score: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    name: str
    description: str
    weight: int


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    course_id: int
    solved: int

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    description: str


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int
    path: str
    unlocked: bool

    class Config:
        orm_mode = True
