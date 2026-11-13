from datetime import datetime
from app import db


class SeatAllocation(db.Model):
    __tablename__ = 'seat_allocations'

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('examination_halls.id'), nullable=False, index=True)
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)
    seat_identifier = db.Column(db.String(25), nullable=False)  # e.g., "H1-R02-C04" or "R2-C4"
    strategy_used = db.Column(db.String(50), default='Sequential', nullable=False)  # Sequential, Random, Mixed Course, Manual
    allocated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    allocated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    examination = db.relationship('Examination', back_populates='allocations')
    student = db.relationship('Student', back_populates='allocations')
    hall = db.relationship('ExaminationHall', back_populates='allocations')
    allocated_by = db.relationship('User', foreign_keys=[allocated_by_id])

    __table_args__ = (
        db.UniqueConstraint('examination_id', 'student_id', name='uq_exam_student_seat'),
        db.UniqueConstraint('examination_id', 'hall_id', 'row_num', 'col_num', name='uq_exam_hall_pos_seat'),
    )

    def __repr__(self):
        return f'<SeatAllocation Exam:{self.examination_id} Student:{self.student_id} Hall:{self.hall_id} Seat:{self.seat_identifier}>'


class AllocationHistory(db.Model):
    __tablename__ = 'allocation_history'

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)  # 'Auto-Allocated', 'Manual Reassigned', 'Cleared', 'Seat Swapped'
    details = db.Column(db.Text, nullable=False)
    performed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    examination = db.relationship('Examination', back_populates='history')
    student = db.relationship('Student')
    performed_by = db.relationship('User')

    def __repr__(self):
        return f'<AllocationHistory {self.action} on Exam {self.examination_id} at {self.timestamp}>'

