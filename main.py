# main.py
from lib.db import Base, engine
from lib.student import Student
from lib.course import Course
from lib.enrolment import Enrollment

print(" Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
