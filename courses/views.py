from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Enrollment
from .serializers import CourseSerializer, CourseProgressSerializer, CertificateSerializer, EnrollmentSerializer
from accounts.permissions import IsTeacher, IsStudent

from .models import CourseProgress, Certificate
from rest_framework.exceptions import PermissionDenied

# --------------------------------------------------

# Teacher: Course CRUD (Create, Update, Delete)

# --------------------------------------------------

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user

        if user.role == "TEACHER":
            return Course.objects.filter(teacher=user)

        return Course.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


# --------------------------------------------------

# Student: Enroll in a Course

# --------------------------------------------------

class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        student = request.user

        try:
            course = Course.objects.get(
                id=course_id,
                is_published=True,
            )
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
        )

        if not created:
            return Response(
                {"error": "Already enrolled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = EnrollmentSerializer(enrollment)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# --------------------------------------------------

# Student: View My Enrolled Courses

# --------------------------------------------------

class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]


    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        courses = [enrollment.course for enrollment in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentCourseListView(APIView): 
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        courses = Course.objects.filter(enrollments__student=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProgressView(APIView): 
    permission_classes = [IsAuthenticated, IsStudent]
    def post(self, request, course_id):
    # Student must be enrolled first
        if not Enrollment.objects.filter(student=request.user, course_id=course_id).exists():
         raise PermissionDenied('You are not enrolled in this course')


        progress, _ = CourseProgress.objects.get_or_create(
        student=request.user,
        course_id=course_id
        )


        progress.status = request.data.get('status', progress.status)
        progress.save()


        return Response({'message': 'Progress updated'}, status=status.HTTP_200_OK)
    

class MyProgressView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        progress = CourseProgress.objects.filter(student=request.user)
        serializer = CourseProgressSerializer(progress, many=True)
        return Response(serializer.data)


class IssueCertificateView(APIView): 
    permission_classes = [IsAuthenticated, IsStudent]
    def post(self, request, course_id):
    # Check enrollment and completion
        if not CourseProgress.objects.filter(student=request.user, course_id=course_id, status='completed').exists():
            raise PermissionDenied('Course not completed yet')


        certificate, created = Certificate.objects.get_or_create(
            student=request.user,
            course_id=course_id
        )


    # Optional: generate file URL (placeholder)
        if not certificate.file_url:
            certificate.file_url = f'/media/certificates/{certificate.id}.pdf'
            certificate.save()


        return Response({'message': 'Certificate issued', 'certificate_url': certificate.file_url}, status=200)
    

class MyCertificatesView(APIView): 
    permission_classes = [IsAuthenticated, IsStudent]
    def get(self, request):
        certificates = Certificate.objects.filter(student=request.user)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data, status=200)
    









    # "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4OTg0NDUzLCJpYXQiOjE3Njg5ODA4NTMsImp0aSI6ImEyNzFmZTIxNTk4YjQxZjU5NGM0N2RhNjhhMWIzOTEyIiwidXNlcl9pZCI6IjEwIn0.mjnFmJZ9FecMIhXNSDo0P7r7yyUeZah1_4ASYNKQCLY",
    # "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2OTA2NzI1MywiaWF0IjoxNzY4OTgwODUzLCJqdGkiOiI5NDcyZGM1ZjFkNTM0OTg4ODlhMjdhMTE4OTc1OGEwOSIsInVzZXJfaWQiOiIxMCJ9.C5ngWWEYBDYJge_ZKAxvr4NIBS4_GGzQikKOStDzUYk",
    # "role": "teacher"