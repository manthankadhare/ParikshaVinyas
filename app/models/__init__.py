from app.models.user import User
from app.models.academic import Department, Course, Subject
from app.models.student import Student
from app.models.hall import ExaminationHall, BlockedSeat
from app.models.exam import Examination, EligibleStudent
from app.models.allocation import SeatAllocation, AllocationHistory
from app.models.invigilator import Invigilator, InvigilatorAssignment
from app.models.qa import TestCase, DefectReport
from app.models.audit import ActivityLog, SystemSetting

__all__ = [
    'User',
    'Department',
    'Course',
    'Subject',
    'Student',
    'ExaminationHall',
    'BlockedSeat',
    'Examination',
    'EligibleStudent',
    'SeatAllocation',
    'AllocationHistory',
    'Invigilator',
    'InvigilatorAssignment',
    'TestCase',
    'DefectReport',
    'ActivityLog',
    'SystemSetting',
]

