from sqlalchemy import create_engine                      # Creates database connection
from sqlalchemy.orm import sessionmaker, declarative_base # Imports ORM utilities
from sqlalchemy.orm import Session                        # For type hinting

# Database connection URL
DATABASE_URL = "mysql+pymysql://root:root123@localhost/fastapi_db"

# Bridge between Python and MySQL
engine = create_engine(DATABASE_URL)

# Base class for all database models
Base = declarative_base()

# Creates new database sessions
SessionLocal = sessionmaker(
    autocommit=False,   # Save changes only after commit()
    autoflush=False,    # Don't sync changes automatically
    bind=engine         # Use this database connection
)

# Provides a database session for each request
def get_db():
    db = SessionLocal()     # Create a new session

    try:
        yield db            # Pass session to FastAPI

    finally:
        db.close()          # Close session after use


# the above func do this to avoid redudancy
# generator = get_db()

# db = next(generator)

# try:
#     get_students(db)
# finally:
#     generator.close()