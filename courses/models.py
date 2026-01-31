from django.db import models 
from django.conf import settings
from accounts.models import User




User = settings.AUTH_USER_MODEL

class Course(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.email} → {self.course.title}"



class CourseProgress(models.Model): 
    STATUS_CHOICES = ( 
        ('not_started', 'Not Started'), 
        ('in_progress', 'In Progress'), 
        ('completed', 'Completed'),
          )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('student', 'course')


class Certificate(models.Model): 
    student = models.ForeignKey(User, on_delete=models.CASCADE) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    issued_at = models.DateTimeField(auto_now_add=True) 
    is_verified = models.BooleanField(default=False) 
    file_url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')



