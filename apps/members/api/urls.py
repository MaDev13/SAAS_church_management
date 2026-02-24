"""Member API URLs."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.MemberListCreateView.as_view(), name="member-list-create"),
    path("<uuid:pk>/", views.MemberDetailView.as_view(), name="member-detail"),
]
