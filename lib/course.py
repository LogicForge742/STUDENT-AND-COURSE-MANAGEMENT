"""
Course Model

Defines the Course entity with SQLAlchemy ORM.
A course can have multiple students enrolled (many-to-many relationship).
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from lib.db import Base


class Course(Base):
    """
    Course Model

    Attributes:
        id (int): Primary key, auto-incremented
        code (str): Unique course code (e.g., 'CS101')
        name (str): Course name (required)
        description (str): Detailed course description
        credits (int): Number of credits for the course
        created_at (datetime): Timestamp when course record was created
        enrollments (relationship): Relationship to Enrollment model
    """
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    credits = Column(Integer, default=3)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to enrollments (one course can have many enrollments)
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Course(id={self.id}, code='{self.code}', name='{self.name}')>"

    def to_dict(self):
        """Convert course object to dictionary"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'credits': self.credits,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }