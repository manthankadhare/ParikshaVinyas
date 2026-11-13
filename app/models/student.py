from datetime import datetime
from app import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)
    enrollment_no = db.Column(db.String(30), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    mobile = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    branch = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    division = db.Column(db.String(10), nullable=False)  # A, B, C, etc.
    academic_year = db.Column(db.String(20), default='2025-2026', nullable=False)
    status = db.Column(db.String(20), default='Active', nullable=False)  # Active, Detained, Inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='student_profile')
    course = db.relationship('Course', back_populates='students')
    allocations = db.relationship('SeatAllocation', back_populates='student', cascade='all, delete-orphan', lazy='dynamic')
    eligible_exams = db.relationship('EligibleStudent', back_populates='student', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.enrollment_no} - {self.full_name}>'

