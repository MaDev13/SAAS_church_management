"""
Church API URLs.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChurchCreateView.as_view(), name="church-create"),
    path("me/", views.ChurchDetailView.as_view(), name="church-detail"),
]
