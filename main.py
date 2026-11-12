from fastapi import FastAPI

from database import Base, engine
from routers.students import router as students_router

# Importing the router also imports the Student model before tables are created.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    version="1.0.0",
    description="A CRUD API for managing student records.",
)

app.include_router(students_router)
