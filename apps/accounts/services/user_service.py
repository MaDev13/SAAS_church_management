"""
User service - business logic for user management.
"""
from apps.accounts.repositories import UserRepository


class UserService:
    """Service for User operations."""

    def __init__(self):
        self.repo = UserRepository()

    def get_user_by_email_church(self, email, church_id):
        return self.repo.get_by_email_and_church(email, church_id)

    def create_user(self, email, password, church=None, role="SECRETARY", **kwargs):
        return self.repo.create_user(
            email=email,
            password=password,
            church=church,
            role=role,
            **kwargs,
        )
