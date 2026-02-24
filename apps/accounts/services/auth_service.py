"""
Auth service - login, token handling.
"""
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.repositories import UserRepository


class AuthService:
    """Service for authentication operations."""

    def __init__(self):
        self.repo = UserRepository()

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "church_id": str(user.church_id) if user.church_id else None,
                "role": user.role,
            },
        }
