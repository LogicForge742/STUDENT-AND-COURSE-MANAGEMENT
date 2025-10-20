import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from lib.db import Base
from lib.student import Student
from lib.course import Course
from lib.enrollment import Enrollment


# ---------------- FIXTURES ----------------
@pytest.fixture(scope="module")
def engine():
    """Create an in-memory SQLite engine for testing."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module")
def tables(engine):
    """Create all tables in the test database."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture()
def session(engine, tables):
    """Provide a fresh session for each test."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


# ---------------- TESTS ----------------

def test_create_student(session):
    """ Ensure a student can be created and stored."""
    student = Student(first_name="John", last_name="Doe", email="john@example.com")
    session.add(student)
    session.commit()

    retrieved = session.query(Student).first()
    assert retrieved.first_name == "John"
    assert retrieved.last_name == "Doe"
    assert retrieved.email == "john@example.com"
    assert isinstance(retrieved.id, int)


def test_unique_email_constraint(session):
    """Ensure duplicate emails raise an IntegrityError."""
    student1 = Student(first_name="Jane", last_name="Smith", email="jane@example.com")
    session.add(student1)
    session.commit()

    duplicate = Student(first_name="Jake", last_name="Stone", email="jane@example.com")
    session.add(duplicate)

    with pytest.raises(Exception):  # Could be IntegrityError
        session.commit()


def test_to_dict_method(session):
    """ Ensure to_dict returns correct dictionary."""
    student = Student(first_name="Sam", last_name="Brown", email="sam@example.com")
    session.add(student)
    session.commit()

    data = student.to_dict()
    assert data["first_name"] == "Sam"
    assert data["last_name"] == "Brown"
    assert data["email"] == "sam@example.com"
    assert "created_at" in data


def test_student_enrollments_relationship(session):
    """ Ensure relationships with enrollments and courses work."""
    student = Student(first_name="Alice", last_name="Miller", email="alice@example.com")
    course = Course(code="CS105", name="Data Structures", description="Intro to data structures")
    session.add_all([student, course])
    session.commit()

    enrollment = Enrollment(student_id=student.id, course_id=course.id, grade="A")
    session.add(enrollment)
    session.commit()

    retrieved_student = session.query(Student).filter_by(email="alice@example.com").first()
    assert len(retrieved_student.enrollments) == 1
    assert retrieved_student.enrollments[0].course.name == "Data Structures"
    assert retrieved_student.enrollments[0].grade == "A"