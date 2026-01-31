from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, EmailOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_email_verified",
        "is_staff",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
                "student_class",
                "role",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "phone_number",
                "student_class",
                "role",
                "password1",
                "password2",
            ),
        }),
    )


admin.site.register(EmailOTP)
