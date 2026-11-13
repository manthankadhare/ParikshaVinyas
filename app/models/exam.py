from datetime import datetime
from app import db


class Examination(db.Model):
    __tablename__ = 'examinations'

    id = db.Column(db.Integer, primary_key=True)
    exam_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    exam_name = db.Column(db.String(150), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    exam_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    exam_type = db.Column(db.String(30), default='Regular', nullable=False)  # Regular, ATKT, Practical, Mid-Term
    academic_year = db.Column(db.String(20), default='2025-2026', nullable=False)
    status = db.Column(db.String(20), default='Scheduled', nullable=False)  # Scheduled, Allocated, In Progress, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    subject = db.relationship('Subject', back_populates='examinations')
    course = db.relationship('Course', back_populates='examinations')
    eligible_students = db.relationship('EligibleStudent', back_populates='examination', cascade='all, delete-orphan', lazy='dynamic')
    allocations = db.relationship('SeatAllocation', back_populates='examination', cascade='all, delete-orphan', lazy='dynamic')
    invigilator_assignments = db.relationship('InvigilatorAssignment', back_populates='examination', cascade='all, delete-orphan', lazy='dynamic')
    history = db.relationship('AllocationHistory', back_populates='examination', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def eligible_count(self):
        return self.eligible_students.count()

    @property
    def allocated_count(self):
        return self.allocations.count()

    @property
    def is_fully_allocated(self):
        return self.eligible_count > 0 and self.eligible_count == self.allocated_count

    def __repr__(self):
        return f'<Examination {self.exam_code}: {self.exam_name} on {self.exam_date}>'


class EligibleStudent(db.Model):
    __tablename__ = 'eligible_students'

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)

    # Relationships
    examination = db.relationship('Examination', back_populates='eligible_students')
    student = db.relationship('Student', back_populates='eligible_exams')

    __table_args__ = (
        db.UniqueConstraint('examination_id', 'student_id', name='uq_exam_student_eligible'),
    )

    def __repr__(self):
        return f'<EligibleStudent Exam:{self.examination_id} Student:{self.student_id}>'

