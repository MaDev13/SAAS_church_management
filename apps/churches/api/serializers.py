"""
Church API serializers.
"""
from rest_framework import serializers
from apps.churches.models import Church


class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = ["id", "name", "city", "country", "created_at"]
        read_only_fields = ["id", "created_at"]


class ChurchCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100, required=False, default="")
    country = serializers.CharField(max_length=100, required=False, default="")
