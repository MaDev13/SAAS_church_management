"""
Tenant-scoped base model for multi-tenant isolation.
All tenant data must inherit from TenantModel.
"""
from django.db import models

from .base import TimeStampedModel


class TenantModel(TimeStampedModel):
    """
    Abstract model for multi-tenant entities.
    Links to Church; all queries must filter by church_id.
    """

    church = models.ForeignKey(
        "churches.Church",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        db_index=True,
    )

    class Meta:
        abstract = True
