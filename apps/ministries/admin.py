from django.contrib import admin
from .models import Ministry


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ["name", "church", "created_at"]
    list_filter = ["church"]
