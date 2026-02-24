"""
Church tenant model - root of multi-tenant hierarchy.
"""
from django.db import models

from apps.core.models import TimeStampedModel


class Church(TimeStampedModel):
    """
    Church (tenant) entity.
    All other tenant-scoped data links to Church via church_id.
    """

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "churches_church"
        verbose_name = "Church"
        verbose_name_plural = "Churches"

    def __str__(self):
        return self.name
