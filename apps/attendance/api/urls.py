"""Attendance API URLs."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.AttendanceListCreateView.as_view(), name="attendance-list-create"),
    path("<uuid:pk>/", views.AttendanceDetailView.as_view(), name="attendance-detail"),
]
