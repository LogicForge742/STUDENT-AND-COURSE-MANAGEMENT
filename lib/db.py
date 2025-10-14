# lib/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#PostgreSQL credentials
DB_USER = "milton"
DB_PASSWORD = "Thanks50:14"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "student_course_management"


# Create the database URL for PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class for all ORM models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Helper function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()