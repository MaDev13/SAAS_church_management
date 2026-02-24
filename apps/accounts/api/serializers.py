"""
Accounts API serializers.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    church_id = serializers.UUIDField(source="church_id", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "church_id", "role", "phone", "first_name", "last_name"]
        read_only_fields = ["id", "email", "church_id"]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    church_id = serializers.UUIDField()
    role = serializers.ChoiceField(
        choices=[c[0] for c in User.role.field.choices],
        default="SECRETARY",
    )
    phone = serializers.CharField(required=False, default="")
    first_name = serializers.CharField(required=False, default="")
    last_name = serializers.CharField(required=False, default="")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    church_id = serializers.UUIDField()
