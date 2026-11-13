from datetime import datetime
from app import db


class Invigilator(db.Model):
    __tablename__ = 'invigilators'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    faculty_id = db.Column(db.String(30), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='Active', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='invigilator_profile')
    assignments = db.relationship('InvigilatorAssignment', back_populates='invigilator', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Invigilator {self.faculty_id} - {self.full_name}>'


class InvigilatorAssignment(db.Model):
    __tablename__ = 'invigilator_assignments'

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('examination_halls.id'), nullable=False)
    invigilator_id = db.Column(db.Integer, db.ForeignKey('invigilators.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='Assigned', nullable=False)  # Assigned, Confirmed, Relieved

    # Relationships
    examination = db.relationship('Examination', back_populates='invigilator_assignments')
    hall = db.relationship('ExaminationHall', back_populates='invigilator_assignments')
    invigilator = db.relationship('Invigilator', back_populates='assignments')

    __table_args__ = (
        db.UniqueConstraint('examination_id', 'hall_id', 'invigilator_id', name='uq_exam_hall_invigilator'),
    )

    def __repr__(self):
        return f'<InvigilatorAssignment Exam:{self.examination_id} Hall:{self.hall_id} Invig:{self.invigilator_id}>'

