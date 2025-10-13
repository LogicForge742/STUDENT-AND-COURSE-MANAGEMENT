"""
Enrollment Model

Defines the Enrollment entity (association table) with SQLAlchemy ORM.
This creates a many-to-many relationship between Students and Courses.
Also stores additional enrollment data like grade and enrollment date.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

class Enrollment(Base):
    """
    Enrollment Model (Association Table with Extra Data)

    Attributes:
        id (int): Primary key, auto-incremented
        student_id (int): Foreign key to students table
        course_id (int): Foreign key to courses table
        grade (str): Student's grade for the course (optional, e.g., 'A', 'B+', etc.)
        enrollment_date (datetime): Timestamp when student enrolled
        student (relationship): Relationship to Student model
        course (relationship): Relationship to Course model
    """
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    grade = Column(String(5))  # Optional: A, A-, B+, B, etc.
    enrollment_date = Column(DateTime, server_default=func.now())

    # Relationships
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

    # Ensure a student can only enroll in a course once
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_student_course'),
    )

    def __repr__(self):
        return f"<Enrollment(id={self.id}, student_id={self.student_id}, course_id={self.course_id}, grade='{self.grade}')>"

    def to_dict(self):
        """Convert enrollment object to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'grade': self.grade,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'student_name': f"{self.student.first_name} {self.student.last_name}" if self.student else None,
            'course_name': self.course.name if self.course else None,
            'course_code': self.course.code if self.course else None
        }
