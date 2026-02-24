"""
Church API views.
"""
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.churches.models import Church
from apps.churches.services import ChurchService
from .serializers import ChurchSerializer, ChurchCreateSerializer


class ChurchCreateView(generics.CreateAPIView):
    """Create a new church (tenant registration)."""

    permission_classes = [AllowAny]
    serializer_class = ChurchCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ChurchService()
        church = service.create_church(
            name=serializer.validated_data["name"],
            city=serializer.validated_data.get("city", ""),
            country=serializer.validated_data.get("country", ""),
        )
        return Response(
            ChurchSerializer(church).data,
            status=status.HTTP_201_CREATED,
        )


class ChurchDetailView(generics.RetrieveAPIView):
    """Retrieve church details (requires auth + church membership)."""

    serializer_class = ChurchSerializer

    def get_object(self):
        from middleware.tenant_context import get_church_id
        church_id = get_church_id()
        if not church_id:
            return None
        return Church.objects.filter(id=church_id).first()
