"""
Attendance admin with "Pasar lista" (take attendance) custom view.
"""
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html
from django.utils import timezone

from .models import Attendance, ServiceType


def pasar_lista_view(request):
    """
    Vista para pasar lista: ver miembros y marcar quién asistió al servicio.
    """
    from apps.members.models import Member
    from apps.churches.models import Church

    if not request.user.is_staff:
        return redirect("admin:login")

    church_id = getattr(request.user, "church_id", None)
    churches = Church.objects.all().order_by("name")

    # Permitir seleccionar iglesia vía GET (para superuser o cambiar iglesia)
    if request.GET.get("church"):
        church_id = request.GET.get("church")

    if not church_id and churches.exists():
        # Si no hay church seleccionada, mostrar selector
        return render(
            request,
            "admin/attendance/pasar_lista_select_church.html",
            {
                "title": "Pasar lista - Seleccionar iglesia",
                "churches": churches,
                "opts": Attendance._meta,
            },
        )

    church_id = church_id or (churches.first().id if churches.exists() else None)
    church = Church.objects.filter(id=church_id).first() if church_id else None

    if not church:
        return render(
            request,
            "admin/attendance/pasar_lista_error.html",
            {"title": "Pasar lista", "message": "No hay iglesias. Cree una primero."},
        )

    # Obtener fecha y tipo de servicio
    today = timezone.localdate()
    selected_date = today
    service_type = ServiceType.DOMINGO_ESCUELA
    service_notes = ""

    if request.method == "POST":
        selected_date_str = request.POST.get("date", str(today))
        service_type = request.POST.get("service_type", ServiceType.DOMINGO_ESCUELA)
        service_notes = request.POST.get("service_notes", "").strip()
        try:
            from datetime import datetime
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            selected_date = today

        # Obtener IDs marcados como presentes
        present_ids = set()
        for key, value in request.POST.items():
            if key.startswith("member_") and value == "on":
                try:
                    present_ids.add(key.replace("member_", ""))
                except (ValueError, TypeError):
                    pass

        # Obtener asistencias actuales para esta fecha y tipo
        current_attendances = Attendance.objects.filter(
            member__church_id=church_id,
            date=selected_date,
            service_type=service_type,
        )

        # Eliminar asistencias de quienes ya no están marcados
        for att in current_attendances:
            if str(att.member_id) not in present_ids:
                att.delete()

        # Crear asistencias para quienes están marcados y no tenían
        existing_member_ids = {str(a.member_id) for a in current_attendances}
        for member_id in present_ids:
            if member_id not in existing_member_ids:
                member = Member.objects.filter(
                    id=member_id, church_id=church_id
                ).first()
                if member:
                    defaults = {}
                    if service_type == ServiceType.OTRO and service_notes:
                        defaults["service_notes"] = service_notes
                    Attendance.objects.get_or_create(
                        member=member,
                        date=selected_date,
                        service_type=service_type,
                        defaults=defaults,
                    )

        return redirect(
            f"{request.path}?church={church_id}&date={selected_date}&service={service_type}&saved=1"
        )

    if request.method == "GET":
        selected_date_str = request.GET.get("date", str(today))
        service_type = request.GET.get("service_type", ServiceType.DOMINGO_ESCUELA)
        service_notes = request.GET.get("service_notes", "")
        try:
            from datetime import datetime
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            selected_date = today

    # Lista de miembros activos de la iglesia
    members = Member.objects.filter(
        church_id=church_id, status="ACTIVE"
    ).order_by("last_name", "first_name")

    # IDs de quienes ya tienen asistencia registrada
    attended_ids = set(
        Attendance.objects.filter(
            member__church_id=church_id,
            date=selected_date,
            service_type=service_type,
        ).values_list("member_id", flat=True)
    )

    context = {
        "title": "Pasar lista",
        "church": church,
        "members": members,
        "attended_ids": attended_ids,
        "selected_date": selected_date,
        "service_type": service_type,
        "service_notes": service_notes,
        "service_choices": ServiceType.choices,
        "opts": Attendance._meta,
        "saved": request.GET.get("saved") == "1",
    }

    return render(request, "admin/attendance/pasar_lista.html", context)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["member", "date", "service_type", "service_notes"]
    list_filter = ["service_type", "date"]
    change_list_template = "admin/attendance/attendance/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "pasar-lista/",
                self.admin_site.admin_view(pasar_lista_view),
                name="attendance_attendance_pasar_lista",
            ),
        ]
        return custom_urls + urls
