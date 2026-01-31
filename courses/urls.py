from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollCourseView, MyCoursesView, StudentCourseListView, MyProgressView, MyCertificatesView, IssueCertificateView

router = DefaultRouter()
router.register('', CourseViewSet)


router.register("courses", CourseViewSet, basename="courses")

urlpatterns = router.urls

urlpatterns = router.urls + [
    path('<int:course_id>/enroll/', EnrollCourseView.as_view()),
    path('my-courses/', MyCoursesView.as_view()),
    path('enrolled/', StudentCourseListView.as_view()),
    path('my-progress/', MyProgressView.as_view()),
    path('my-certificates/', MyCertificatesView.as_view()),
    path('<int:course_id>/certificate/', IssueCertificateView.as_view()),
     path(
        "courses/<int:course_id>/enroll/",
        EnrollCourseView.as_view(),
        name="course-enroll",
    ),
]
