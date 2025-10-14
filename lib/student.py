"""
Student Model

Defines the Student entity with SQLAlchemy ORM.
A student can enroll in multiple courses (many-to-many relationship).
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from lib.db import Base

class Student(Base):
    """
    Student Model

    Attributes:
        id (int): Primary key, auto-incremented
        first_name (str): Student's first name (required)
        last_name (str): Student's last name (required)
        email (str): Student's email address (unique, required)
        created_at (datetime): Timestamp when student record was created
        enrollments (relationship): Relationship to Enrollment model
    """
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to enrollments (one student can have many enrollments)
    enrollments = relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.first_name} {self.last_name}', email='{self.email}')>"

    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }