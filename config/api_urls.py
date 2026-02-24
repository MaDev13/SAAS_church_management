"""
API v1 URL routing.
"""
from django.urls import path, include

urlpatterns = [
    path("auth/", include("apps.accounts.api.urls")),
    path("churches/", include("apps.churches.api.urls")),
    path("ministries/", include("apps.ministries.api.urls")),
    path("members/", include("apps.members.api.urls")),
    path("attendance/", include("apps.attendance.api.urls")),
]
