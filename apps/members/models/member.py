"""
Member model - church member with demographics and ministry assignment.
"""
from datetime import date

from django.db import models

from apps.core.models import TenantModel
from apps.core.managers import TenantManager


class MemberStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"


class MaritalStatus(models.TextChoices):
    SINGLE = "SINGLE", "Single"
    MARRIED = "MARRIED", "Married"
    DIVORCED = "DIVORCED", "Divorced"
    WIDOWED = "WIDOWED", "Widowed"


class Member(TenantModel):
    """Church member."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    marital_status = models.CharField(
        max_length=20, choices=MaritalStatus.choices, blank=True
    )
    join_date = models.DateField(null=True, blank=True)
    ministry = models.ForeignKey(
        "ministries.Ministry",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices,
        default=MemberStatus.ACTIVE,
    )

    objects = TenantManager()

    class Meta:
        db_table = "members_member"
        verbose_name = "Member"
        verbose_name_plural = "Members"
        indexes = [
            models.Index(fields=["church", "status"]),
            models.Index(fields=["church", "join_date"]),
            models.Index(fields=["church", "ministry"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        """Edad actual en años (calculada desde birth_date)."""
        if not self.birth_date:
            return None
        today = date.today()
        age_years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age_years -= 1
        return age_years

    @property
    def next_age(self):
        """Edad que cumplirá en su próximo cumpleaños."""
        if not self.birth_date:
            return None
        return self.age + 1 if self.age is not None else None
