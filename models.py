from sqlalchemy import Column, Integer, String    # Imports column and data types

from database import Base                         # Base class for all database tables


# Student table in the database
class Student(Base):

    __tablename__ = "students"                    # Name of the table in MySQL

    id = Column(Integer, primary_key=True, index=True)  # Primary key (unique ID)
    name = Column(String(100))                    # Student name (max 100 characters)
    age = Column(Integer)                         # Student age
    course = Column(String(100))                  # Student course (max 100 characters)