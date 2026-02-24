"""
Accounts API views - auth, register.
"""
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from apps.accounts.services import AuthService, UserService
from apps.churches.models import Church
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    """Register a new user for a church."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        church = Church.objects.filter(id=data["church_id"]).first()
        if not church:
            return Response(
                {"church_id": "Church not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = UserService()
        if service.get_user_by_email_church(data["email"], church.id):
            return Response(
                {"email": "User with this email already exists in this church."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = service.create_user(
            email=data["email"],
            password=data["password"],
            church=church,
            role=data.get("role", "SECRETARY"),
            phone=data.get("phone", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )
        auth_service = AuthService()
        tokens = auth_service.get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login - returns JWT tokens."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.filter(
            email=data["email"],
            church_id=data["church_id"],
        ).first()
        if user is None or not user.check_password(data["password"]):
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        auth_service = AuthService()
        tokens = auth_service.get_tokens_for_user(user)
        return Response(tokens)


class MeView(APIView):
    """Current user profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
