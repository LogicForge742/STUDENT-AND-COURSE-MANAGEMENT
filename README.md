# Student & Course Management

A Python application that models a student/course domain using SQLAlchemy ORM with a many-to-many relationship via an Enrollment association. It includes unit tests and a simple bootstrap script to create database tables.

## Features
- SQLAlchemy ORM models for:
  - Student (unique email, created_at)
  - Course (unique code, credits, created_at)
  - Enrollment (joins Student and Course; unique student/course pair; grade, enrollment_date)
- PostgreSQL connection (configurable in `lib/db.py`)
- One-step database bootstrap via `main.py`
- Pytest-based test suite using in-memory SQLite for fast testing

## Tech stack
- Python 3.10+
- SQLAlchemy 2.x
- PostgreSQL (via `psycopg2-binary`)
- Pytest

## Project structure
```
STUDENT-AND-COURSE-MANAGEMENT/
├─ lib/
│  ├─ __init__.py
│  ├─ db.py            # DB engine, Base, Session
│  ├─ student.py       # Student model
│  ├─ course.py        # Course model
│  ├─ enrollment.py    # Enrollment model (association)
│  └─ cli.py           # (placeholder for future CLI)
├─ tests/
│  ├─ test_course.py
│  ├─ test_enrollment.py
│  ├─ test_hello.py
│  └─ test_student.py
├─ main.py             # Creates tables in the configured DB
├─ requirements.txt
├─ pytest.ini
└─ README.md
```

## Quick start

1) Prerequisites
- Python 3.10+
- PostgreSQL 13+ installed and running
- A PostgreSQL user and database you can connect to

2) Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies
```
pip install -r requirements.txt
```

4) Configure the database connection
- Open `lib/db.py` and confirm or change:
  - `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
- The default URL is built as:
```
postgresql+psycopg2://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```
- For example, to mirror the current defaults in `lib/db.py`, you can create matching credentials in PostgreSQL:
```
psql -U postgres -c "CREATE USER milton WITH PASSWORD 'Thanks50:14';"
psql -U postgres -c "CREATE DATABASE student_course_management OWNER milton;"
```
Note: Hardcoded credentials in source are for local development only. Prefer environment variables or a secrets manager for real deployments.

5) Initialize the database schema
```
python main.py
```
You should see output indicating tables were created.

## Running tests
The test suite uses in-memory SQLite to stay fast and isolated from your PostgreSQL instance.
```
pytest -q
```

## Data model overview
- Student
  - id (PK, autoincrement)
  - first_name (required)
  - last_name (required)
  - email (unique, required)
  - created_at (server default NOW)
  - enrollments: relationship to Enrollment (cascade delete)
- Course
  - id (PK, autoincrement)
  - code (unique, required, e.g., CS101)
  - name (required)
  - description (optional)
  - credits (default 3)
  - created_at (server default NOW)
  - enrollments: relationship to Enrollment (cascade delete)
- Enrollment (association table with extra data)
  - id (PK, autoincrement)
  - student_id (FK→students.id, NOT NULL)
  - course_id (FK→courses.id, NOT NULL)
  - grade (optional, e.g., A, B+)
  - enrollment_date (server default NOW)
  - UniqueConstraint(student_id, course_id)

## Usage examples
Below is a simple interactive session pattern you can adapt in your own scripts. It uses the `SessionLocal` factory defined in `lib/db.py`.

1) Open a Python shell with your virtual environment active, then run:
```python
from lib.db import SessionLocal
from lib.student import Student
from lib.course import Course
from lib.enrollment import Enrollment

session = SessionLocal()

# Create a student and a course
student = Student(first_name="Ada", last_name="Lovelace", email="ada@example.com")
course = Course(code="CS101", name="Intro to Computer Science", description="Basics of computing", credits=4)
session.add_all([student, course])
session.commit()

# Enroll the student
enrollment = Enrollment(student_id=student.id, course_id=course.id, grade="A")
session.add(enrollment)
session.commit()

# Query back
enrolled = session.query(Enrollment).first()
print(enrolled, enrolled.student.first_name, enrolled.course.name)

session.close()
```

## Development notes
- `lib/cli.py` is a placeholder for future command-line utilities (e.g., CRUD commands). You can implement a CLI using `argparse` or `typer` that uses the existing models and `SessionLocal`.
- Tests demonstrate how to run the models against SQLite in-memory databases. This is useful for fast feedback.
- For production-grade workflows, consider:
  - Using environment variables for DB settings (and reading them in `lib/db.py`)
  - Adding Alembic migrations
  - Creating an API layer (e.g., FastAPI) or a CLI for operations
  - Input validation and more robust error handling

## Troubleshooting
- psycopg2.OperationalError / connection refused
  - Ensure PostgreSQL is running and credentials in `lib/db.py` are correct
  - Verify the DB exists and your user has privileges
- psycopg2.ProgrammingError on first run
  - Make sure you have run `python main.py` to create tables
- Unique constraint violations
  - Student emails and course codes must be unique
  - A student can only enroll in a specific course once
- Import errors
  - Run from the project root and ensure the virtual environment is activated

## License
This project is licensed under the [MIT License]

