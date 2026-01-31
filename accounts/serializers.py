from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "student_class",
            "role",
            "password",
            "confirm_password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")

        if data["role"] == "STUDENT" and not data.get("student_class"):
            raise serializers.ValidationError("Student class is required")

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            email=data.get("email"),
            password=data.get("password"),
        )

        if not user:
            raise serializers.ValidationError("Invalid login credentials")

        if not user.is_email_verified:
            raise serializers.ValidationError("Email is not verified")

        data["user"] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
