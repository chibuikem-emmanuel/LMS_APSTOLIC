from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, EmailOTP
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .utils import generate_otp, send_otp_email


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)
        send_otp_email(user.email, otp)

        return Response({"message": "OTP sent to email"})


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        record = EmailOTP.objects.filter(user=user, otp=otp).first()
        if not record:
            return Response({"error": "Invalid OTP"}, status=400)

        user.is_email_verified = True
        user.save()
        record.delete()

        return Response({"message": "Email verified successfully"})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                "role": user.role,
            },
        })


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        otp = generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)
        send_otp_email(user.email, otp)

        return Response({"message": "Password reset OTP sent"})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        record = EmailOTP.objects.filter(user=user, otp=otp).first()
        if not record:
            return Response({"error": "Invalid OTP"}, status=400)

        user.set_password(new_password)
        user.save()
        record.delete()

        return Response({"message": "Password reset successful"})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        })
