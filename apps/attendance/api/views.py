"""Attendance API views."""

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from apps.attendance.models import Attendance
from apps.attendance.services import AttendanceService
from .serializers import AttendanceSerializer


class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["member", "date", "service_type"]

    def get_queryset(self):
        return AttendanceService().list_for_church()

    def perform_create(self, serializer):
        data = serializer.validated_data
        att = AttendanceService().create(
            member_id=data["member"].id,
            date=data["date"],
            service_type=data.get("service_type", "SUNDAY"),
        )
        serializer.instance = att


class AttendanceDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        return AttendanceService().list_for_church()
