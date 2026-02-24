from django.contrib import admin
from .models import Church


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "city", "country", "created_at"]
    search_fields = ["name", "city", "country"]
