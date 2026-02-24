"""
User repository - data access layer.
"""
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository:
    """Repository for User CRUD operations."""

    @staticmethod
    def get_by_email_and_church(email, church_id):
        return User.objects.filter(email=email, church_id=church_id).first()

    @staticmethod
    def get_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def create_user(email, password, church=None, role="SECRETARY", **kwargs):
        return User.objects.create_user(
            email=email,
            password=password,
            church=church,
            role=role,
            username=email,
            **kwargs,
        )
