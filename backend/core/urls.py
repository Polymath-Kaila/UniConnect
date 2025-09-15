from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, MeView,
    UniversityViewSet, UserViewSet, CohortViewSet, CourseViewSet,
    EnrollmentViewSet, GroupViewSet, GroupMemberViewSet,
    ProjectViewSet, ProjectTaskViewSet, ConnectionViewSet
)

router = DefaultRouter()
router.register(r"universities", UniversityViewSet, basename="university")
router.register(r"users", UserViewSet, basename="user")
router.register(r"cohorts", CohortViewSet, basename="cohort")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"group-members", GroupMemberViewSet, basename="groupmember")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", ProjectTaskViewSet, basename="task")
router.register(r"connections", ConnectionViewSet, basename="connection")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
