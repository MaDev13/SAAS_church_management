"""Ministry serializers."""

from rest_framework import serializers
from apps.ministries.models import Ministry


class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]
