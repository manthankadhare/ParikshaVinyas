from datetime import datetime
from app import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    courses = db.relationship('Course', back_populates='department_rel', lazy='dynamic')

    def __repr__(self):
        return f'<Department {self.code}: {self.name}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    total_semesters = db.Column(db.Integer, default=8, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    department_rel = db.relationship('Department', back_populates='courses')
    subjects = db.relationship('Subject', back_populates='course', cascade='all, delete-orphan', lazy='dynamic')
    students = db.relationship('Student', back_populates='course', lazy='dynamic')
    examinations = db.relationship('Examination', back_populates='course', lazy='dynamic')

    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, default=4, nullable=False)
    academic_year = db.Column(db.String(20), default='2025-2026')

    # Relationships
    course = db.relationship('Course', back_populates='subjects')
    examinations = db.relationship('Examination', back_populates='subject', lazy='dynamic')

    def __repr__(self):
        return f'<Subject {self.code}: {self.name} (Sem {self.semester})>'

