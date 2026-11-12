from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_db
from models import Student


router = APIRouter(prefix="/students", tags=["students"])


class StudentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0)
    course: str = Field(min_length=1, max_length=100)


class StudentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0)
    course: str | None = Field(default=None, min_length=1, max_length=100)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    course: str


def get_student_or_404(student_id: int, db: Session) -> Student:
    try:
        student = db.get(Student, student_id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        ) from None

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


def commit_and_refresh(student: Student, db: Session) -> Student:
    try:
        db.commit()
        db.refresh(student)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        ) from None
    return student


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    return commit_and_refresh(new_student, db)


@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    try:
        return db.query(Student).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        ) from None


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_or_404(student_id, db)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student_data: StudentCreate, db: Session = Depends(get_db)
):
    student = get_student_or_404(student_id, db)
    for field, value in student_data.model_dump().items():
        setattr(student, field, value)
    return commit_and_refresh(student, db)


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student_partially(
    student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)
):
    student = get_student_or_404(student_id, db)
    updates = student_data.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in updates.items():
        setattr(student, field, value)
    return commit_and_refresh(student, db) if updates else student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    try:
        db.delete(student)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        ) from None
    return {"message": "Student deleted successfully"}
