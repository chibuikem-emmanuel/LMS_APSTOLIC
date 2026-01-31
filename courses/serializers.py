from rest_framework import serializers 
from .models import Course, Enrollment, CourseProgress, Certificate

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "is_published",
            "created_at",
        )



class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = (
            "id",
            "course",
            "enrolled_at",
        )
        read_only_fields = ("enrolled_at",)


class CourseProgressSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CourseProgress 
        fields = 'all'


class CertificateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Certificate 
        fields = 'all'