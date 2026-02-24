"""
Attendance model - member attendance records.
"""
from django.db import models

from apps.core.models import TimeStampedModel


class ServiceType(models.TextChoices):
    DOMINGO_ESCUELA = "DOMINGO_ESCUELA", "Domingo - Escuela dominical"
    MARTES_ORACION = "MARTES_ORACION", "Martes - De oración"
    JUEVES_CLAMOR = "JUEVES_CLAMOR", "Jueves - Clamor y adoración"
    MIERCOLES_AYUNO = "MIERCOLES_AYUNO", "Miércoles - Ayuno"
    SABADO_AYUNO = "SABADO_AYUNO", "Sábado - Ayuno"
    OTRO = "OTRO", "Otro (escribir)"


class Attendance(TimeStampedModel):
    """Attendance record for a member on a date."""

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="attendances",
        db_index=True,
    )
    date = models.DateField(db_index=True)
    service_type = models.CharField(
        max_length=30,
        choices=ServiceType.choices,
        default=ServiceType.DOMINGO_ESCUELA,
    )
    service_notes = models.CharField(
        max_length=100,
        blank=True,
        help_text="Descripción cuando el tipo es 'Otro'",
    )

    class Meta:
        db_table = "attendance_attendance"
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        indexes = [
            models.Index(fields=["member", "date"]),
            models.Index(fields=["date"]),
        ]
        unique_together = [["member", "date", "service_type"]]
