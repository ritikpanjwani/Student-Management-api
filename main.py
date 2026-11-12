from fastapi import FastAPI, Depends, HTTPException      # FastAPI classes
from pydantic import BaseModel                           # Used for request/response validation
from sqlalchemy.orm import Session                       # Database session

from database import engine, get_db                      # Database connection
from models import Base, Student                         # Student table (ORM model)

# Create the tables in MySQL if they don't already exist
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI()


# ==========================================================
#               Pydantic Schemas
# ==========================================================

# Used when creating a new student
class StudentCreate(BaseModel):
    name: str
    age: int
    course: str


# Used for PATCH (all fields optional)
class UpdateStudentCreate(BaseModel):
    name: str | None = None
    age: int | None = None
    course: str | None = None


# Used when sending data back to the client
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str

    class Config:
        from_attributes = True      # Convert SQLAlchemy object into JSON


# ==========================================================
#               CREATE STUDENT (POST)
# ==========================================================

@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,              # Data received from client
    db: Session = Depends(get_db)        # Get database session
):

    # Create SQLAlchemy object
    new_student = Student(
        name=student.name,
        age=student.age,
        course=student.course
    )

    # Add object to database session
    db.add(new_student)

    # Save data to MySQL
    db.commit()

    # Refresh object to get generated ID
    db.refresh(new_student)

    # Return created student
    return new_student


# ==========================================================
#               GET ALL STUDENTS
# ==========================================================

@app.get("/students", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):

    # Fetch all students from database
    students = db.query(Student).all()

    return students


# ==========================================================
#               GET STUDENT BY ID
# ==========================================================

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Find student by ID
    student = db.query(Student).filter(Student.id == student_id).first()

    # If student doesn't exist
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ==========================================================
#               UPDATE ENTIRE STUDENT (PUT)
# ==========================================================

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    studentnew: StudentCreate,
    db: Session = Depends(get_db)
):

    # Find student
    student = db.query(Student).filter(Student.id == student_id).first()

    # If not found
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Replace all values
    student.name = studentnew.name
    student.age = studentnew.age
    student.course = studentnew.course

    # Save changes
    db.commit()

    # Refresh object
    db.refresh(student)

    return student


# ==========================================================
#               DELETE STUDENT
# ==========================================================

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Find student
    student = db.query(Student).filter(Student.id == student_id).first()

    # If student doesn't exist
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Delete student
    db.delete(student)

    # Save changes
    db.commit()

    return {
        "message": "Student deleted successfully"
    }


# ==========================================================
#               UPDATE SOME FIELDS (PATCH)
# ==========================================================

@app.patch("/students/{student_id}", response_model=StudentResponse)
def update_parts(
    student_id: int,
    studentsome: UpdateStudentCreate,          # Optional fields
    db: Session = Depends(get_db)
):

    # Find student
    student = db.query(Student).filter(Student.id == student_id).first()

    # If student doesn't exist
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Update only name if provided
    if studentsome.name is not None:
        student.name = studentsome.name

    # Update only age if provided
    if studentsome.age is not None:
        student.age = studentsome.age

    # Update only course if provided
    if studentsome.course is not None:
        student.course = studentsome.course

    # Save changes
    db.commit()

    # Refresh object
    db.refresh(student)

    return student