from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели Пользователь."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "address",
            "birth_date",
            "is_librarian",
            "is_active",
        ]
        read_only_fields = ["is_librarian", "is_active"]


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя и управления аккаунтами."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password2",
            "phone",
            "address",
            "birth_date",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user
