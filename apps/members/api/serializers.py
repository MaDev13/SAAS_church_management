"""Member serializers."""

from rest_framework import serializers
from apps.members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    ministry_name = serializers.SerializerMethodField()

    def get_ministry_name(self, obj):
        return obj.ministry.name if obj.ministry else None

    class Meta:
        model = Member
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "address",
            "birth_date",
            "gender",
            "marital_status",
            "join_date",
            "ministry",
            "ministry_name",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
