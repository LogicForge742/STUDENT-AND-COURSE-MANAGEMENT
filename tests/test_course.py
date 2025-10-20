import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db import Base
from lib.course import Course

# ---------- Setup ----------
@pytest.fixture(scope="module")
def session():
    """Create an in-memory SQLite session for testing"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

# ---------- Tests ----------

def test_create_course(session):
    """Test that a course can be created and saved"""
    course = Course(code="CS101", name="Intro to Computer Science", description="Basics of computing", credits=4)
    session.add(course)
    session.commit()

    saved_course = session.query(Course).filter_by(code="CS101").first()
    assert saved_course is not None
    assert saved_course.name == "Intro to Computer Science"
    assert saved_course.credits == 4

def test_course_repr():
    """Test string representation"""
    course = Course(id=1, code="CS101", name="Intro to Computer Science")
    assert "<Course(id=1, code='CS101', name='Intro to Computer Science')>" in repr(course)

def test_to_dict():
    """Test conversion to dictionary"""
    course = Course(code="CS102", name="Data Structures", description="Learn data structures", credits=3)
    course_dict = course.to_dict()
    assert course_dict["code"] == "CS102"
    assert course_dict["name"] == "Data Structures"
    assert "created_at" in course_dict
