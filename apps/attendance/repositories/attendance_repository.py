"""Attendance repository."""

from django.db.models import Count
from django.db.models.functions import TruncDate

from apps.attendance.models import Attendance
from apps.members.models import Member


class AttendanceRepository:
    @staticmethod
    def create(member_id, date, service_type="SUNDAY"):
        return Attendance.objects.create(
            member_id=member_id, date=date, service_type=service_type
        )

    @staticmethod
    def list_for_member(member_id):
        return Attendance.objects.filter(member_id=member_id).order_by("-date")

    @staticmethod
    def list_for_church(church_id, date_from=None, date_to=None):
        qs = Attendance.objects.filter(member__church_id=church_id)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs.order_by("-date")
