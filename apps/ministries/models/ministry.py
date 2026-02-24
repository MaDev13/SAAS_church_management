"""
Ministry model - groups/teams within a church.
"""
from django.db import models

from apps.core.models import TenantModel
from apps.core.managers import TenantManager


class Ministry(TenantModel):
    """Ministry within a church."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    objects = TenantManager()

    class Meta:
        db_table = "ministries_ministry"
        verbose_name = "Ministry"
        verbose_name_plural = "Ministries"
        indexes = [
            models.Index(fields=["church", "name"]),
        ]

    def __str__(self):
        return self.name
