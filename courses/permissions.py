from rest_framework.permissions import BasePermission



class IsTeacher(BasePermission):
    """
    Allows access only to users with TEACHER role.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.role == "TEACHER"
            and user.is_email_verified
        )
    


class IsStudent(BasePermission):
    """
    Allows access only to verified students.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.role == "STUDENT"
            and user.is_email_verified
        )