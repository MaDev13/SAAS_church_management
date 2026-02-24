"""Ministry API views."""

from rest_framework import generics
from apps.ministries.models import Ministry
from apps.ministries.services import MinistryService
from .serializers import MinistrySerializer


class MinistryListCreateView(generics.ListCreateAPIView):
    serializer_class = MinistrySerializer

    def get_queryset(self):
        return MinistryService().list()

    def perform_create(self, serializer):
        svc = MinistryService()
        ministry = svc.create(
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", ""),
        )
        serializer.instance = ministry


class MinistryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MinistrySerializer

    def get_queryset(self):
        return MinistryService().list()
