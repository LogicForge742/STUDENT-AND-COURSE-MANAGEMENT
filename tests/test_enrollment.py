import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.db import Base
from lib.student import Student
from lib.course import Course
from lib.enrollment import Enrollment


# --- Setup temporary SQLite database for testing ---
@pytest.fixture(scope="module")
def session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


# --- Tests ---

def test_create_enrollment(session):
    """ Test that an enrollment can be created successfully"""
    student = Student(first_name="John", last_name="Doe", email="john@example.com")
    course = Course(code="CS101", name="Intro to Programming", description="Basic Python", credits=3)

    session.add_all([student, course])
    session.commit()

    enrollment = Enrollment(student_id=student.id, course_id=course.id, grade="A")
    session.add(enrollment)
    session.commit()

    result = session.query(Enrollment).first()
    assert result is not None
    assert result.grade == "A"
    assert result.student_id == student.id
    assert result.course_id == course.id


def test_unique_student_course_constraint(session):
    """Test that a student cannot enroll in the same course twice"""
    student = Student(first_name="Jane", last_name="Doe", email="jane@example.com")
    course = Course(code="CS102", name="Data Structures", description="Learn data structures", credits=4)
    session.add_all([student, course])
    session.commit()

    # First enrollment succeeds
    enrollment1 = Enrollment(student_id=student.id, course_id=course.id, grade="B")
    session.add(enrollment1)
    session.commit()

    # Second identical enrollment should fail
    enrollment2 = Enrollment(student_id=student.id, course_id=course.id, grade="A")
    session.add(enrollment2)
    with pytest.raises(Exception):  # IntegrityError due to UniqueConstraint
        session.commit()
    session.rollback()


def test_enrollment_relationships(session):
    """Test that relationships link properly between Student, Course, and Enrollment"""
    student = Student(first_name="Sam", last_name="Smith", email="sam@example.com")
    course = Course(code="CS103", name="Algorithms", description="Algorithm design", credits=3)
    session.add_all([student, course])
    session.commit()

    enrollment = Enrollment(student_id=student.id, course_id=course.id, grade="B+")
    session.add(enrollment)
    session.commit()

    #  Query only the enrollment we just added
    retrieved = session.query(Enrollment).filter_by(student_id=student.id, course_id=course.id).first()
    assert retrieved.student.first_name == "Sam"
    assert retrieved.course.name == "Algorithms"

def test_to_dict_method(session):
    """ Test the to_dict method returns correct dictionary representation"""
    student = Student(first_name="Alice", last_name="Wang", email="alice@example.com")
    course = Course(code="CS104", name="Databases", description="Intro to SQL", credits=3)
    session.add_all([student, course])
    session.commit()

    enrollment = Enrollment(student_id=student.id, course_id=course.id, grade="A-")
    session.add(enrollment)
    session.commit()

    data = enrollment.to_dict()
    assert isinstance(data, dict)
    assert data["student_id"] == student.id
    assert data["course_id"] == course.id
    assert "student_name" in data
    assert "course" not in data  # make sure nested ORM objects aren’t returned
