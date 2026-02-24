"""Ministry API URLs."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.MinistryListCreateView.as_view(), name="ministry-list-create"),
    path("<uuid:pk>/", views.MinistryDetailView.as_view(), name="ministry-detail"),
]
