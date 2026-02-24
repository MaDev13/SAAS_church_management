from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "age_display",
        "next_age_display",
        "church",
        "status",
        "ministry",
    ]
    list_filter = ["church", "status", "ministry"]
    readonly_fields = ["age_display", "next_age_display"]
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "church", "status", "ministry")}),
        ("Contacto", {"fields": ("phone", "address")}),
        (
            "Información personal",
            {
                "fields": (
                    "birth_date",
                    "age_display",
                    "next_age_display",
                    "gender",
                    "marital_status",
                ),
            },
        ),
        ("Historial", {"fields": ("join_date", "created_at", "updated_at")}),
    )

    def age_display(self, obj):
        """Edad actual del miembro."""
        age = obj.age
        return f"{age} años" if age is not None else "—"

    age_display.short_description = "Edad"

    def next_age_display(self, obj):
        """Edad que cumplirá en su próximo cumpleaños."""
        next_age = obj.next_age
        return f"cumplirá {next_age} años" if next_age is not None else "—"

    next_age_display.short_description = "Próximo cumpleaños"
