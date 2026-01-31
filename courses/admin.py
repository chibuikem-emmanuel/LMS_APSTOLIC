from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "teacher",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "teacher__email",
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "teacher",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "course",
        "enrolled_at",
    )

    list_filter = (
        "enrolled_at",
    )

    search_fields = (
        "student__email",
        "course__title",
    )

    ordering = ("-enrolled_at",)

    autocomplete_fields = (
        "student",
        "course",
    )

    readonly_fields = (
        "enrolled_at",
    )
