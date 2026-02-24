"""
Custom User model extending AbstractUser.
Multi-tenant: each user belongs to a Church.
Login uses email instead of username.
"""
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager que usa email como identificador de login."""

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        kwargs.setdefault("username", email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("username", email)
        return self.create_user(email, password, **kwargs)


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Admin"
    LEADER = "LEADER", "Leader"
    SECRETARY = "SECRETARY", "Secretary"


class User(AbstractUser):
    """
    Custom user with church (tenant), role, and phone.
    id is UUID. church can be null for SUPER_ADMIN (platform-wide).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("email", unique=True)
    church = models.ForeignKey(
        "churches.Church",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users",
        db_index=True,
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.SECRETARY,
    )
    phone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "accounts_user"
        indexes = [
            models.Index(fields=["church", "email"]),
            models.Index(fields=["church"]),
        ]
