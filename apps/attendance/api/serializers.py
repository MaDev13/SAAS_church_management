"""Attendance serializers."""

from rest_framework import serializers
from apps.attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()

    def get_member_name(self, obj):
        return str(obj.member) if obj.member else None

    class Meta:
        model = Attendance
        fields = ["id", "member", "member_name", "date", "service_type", "created_at"]
        read_only_fields = ["id", "created_at"]
