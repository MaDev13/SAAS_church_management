"""Member API views."""

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.members.models import Member
from apps.members.services import MemberService
from .serializers import MemberSerializer


class MemberListCreateView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["status", "ministry"]
    search_fields = ["first_name", "last_name"]

    def get_queryset(self):
        return MemberService().list()

    def perform_create(self, serializer):
        member = MemberService().create(**serializer.validated_data)
        serializer.instance = member


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer

    def get_queryset(self):
        return MemberService().list()
