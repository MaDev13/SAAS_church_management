from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "church", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    filter_horizontal = []

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Nombre para mostrar", {"fields": ("first_name", "last_name"), "description": "Estos campos se muestran en la barra del admin en lugar del correo."}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "role")}),
        ("Iglesia", {"fields": ("church", "phone")}),
        ("Fechas", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        ("Info", {"fields": ("first_name", "last_name", "church", "role", "phone")}),
    )
