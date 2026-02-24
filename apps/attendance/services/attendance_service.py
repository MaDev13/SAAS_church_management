"""Attendance service."""

from apps.attendance.models import Attendance
from apps.attendance.repositories import AttendanceRepository
from apps.members.repositories import MemberRepository
from middleware.tenant_context import get_church_id


class AttendanceService:
    def __init__(self):
        self.repo = AttendanceRepository()
        self.member_repo = MemberRepository()

    def create(self, member_id, date, service_type="SUNDAY"):
        church_id = get_church_id()
        if not church_id:
            raise ValueError("Church context required")
        member = self.member_repo.get_by_id(member_id, church_id)
        if not member:
            raise ValueError("Member not found")
        return self.repo.create(member_id=member_id, date=date, service_type=service_type)

    def list_for_member(self, member_id):
        church_id = get_church_id()
        if not church_id:
            return Attendance.objects.none()
        member = self.member_repo.get_by_id(member_id, church_id)
        if not member:
            return Attendance.objects.none()
        return self.repo.list_for_member(member_id)

    def list_for_church(self, date_from=None, date_to=None):
        church_id = get_church_id()
        if not church_id:
            return Attendance.objects.none()
        return self.repo.list_for_church(church_id, date_from, date_to)
