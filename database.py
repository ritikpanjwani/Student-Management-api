from sqlalchemy import create_engine                      # Creates database connection
from sqlalchemy.orm import sessionmaker, declarative_base # Imports ORM utilities
from sqlalchemy.orm import Session                        # For type hinting
from dotenv import load_dotenv
import os

# Load local configuration from .env (without overwriting real environment values).
load_dotenv()

# Database connection URL. Set DATABASE_URL in .env before starting the app.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Copy .env.example to .env and set it."
    )

# Bridge between Python and MySQL. Pool checks prevent stale connections.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

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
