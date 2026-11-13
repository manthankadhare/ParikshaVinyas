from datetime import datetime
from app import db


class ExaminationHall(db.Model):
    __tablename__ = 'examination_halls'

    id = db.Column(db.Integer, primary_key=True)
    hall_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    hall_name = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.String(20), nullable=False)
    num_rows = db.Column(db.Integer, nullable=False)
    num_cols = db.Column(db.Integer, nullable=False)
    total_capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Active', nullable=False)  # Active, Maintenance, Inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    blocked_seats = db.relationship('BlockedSeat', back_populates='hall', cascade='all, delete-orphan', lazy='dynamic')
    allocations = db.relationship('SeatAllocation', back_populates='hall', lazy='dynamic')
    invigilator_assignments = db.relationship('InvigilatorAssignment', back_populates='hall', lazy='dynamic')

    @property
    def blocked_count(self):
        return self.blocked_seats.count()

    @property
    def usable_capacity(self):
        return max(0, self.total_capacity - self.blocked_count)

    def is_seat_blocked(self, row, col):
        return self.blocked_seats.filter_by(row_num=row, col_num=col).first() is not None

    def __repr__(self):
        return f'<ExaminationHall {self.hall_code}: {self.hall_name} ({self.usable_capacity}/{self.total_capacity})>'


class BlockedSeat(db.Model):
    __tablename__ = 'blocked_seats'

    id = db.Column(db.Integer, primary_key=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('examination_halls.id'), nullable=False)
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)
    seat_identifier = db.Column(db.String(20), nullable=False)  # e.g., "R1-C4"
    reason = db.Column(db.String(200), default='Damaged / Reserved')
    blocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    hall = db.relationship('ExaminationHall', back_populates='blocked_seats')

    __table_args__ = (
        db.UniqueConstraint('hall_id', 'row_num', 'col_num', name='uq_hall_row_col_blocked'),
    )

    def __repr__(self):
        return f'<BlockedSeat {self.seat_identifier} in Hall {self.hall_id}>'

