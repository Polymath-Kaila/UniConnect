from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import University, Cohort, Course, Enrollment, Group, GroupMember, Project, ProjectTask, Connection
from .serializers import (
    UniversitySerializer, CohortSerializer, CourseSerializer, EnrollmentSerializer,
    GroupSerializer, GroupMemberSerializer, ProjectSerializer, ProjectTaskSerializer, ConnectionSerializer,
    UserSerializer
)
from .permissions import IsSelfOrReadOnly, IsTeacher

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(
            username=serializer.validated_data.get("username"),
            email=serializer.validated_data.get("email"),
            display_name=serializer.validated_data.get("display_name",""),
            role=serializer.validated_data.get("role","student"),
            university=serializer.validated_data.get("university"),
            mentor=serializer.validated_data.get("mentor"),
            year_of_study=serializer.validated_data.get("year_of_study"),
            bio=serializer.validated_data.get("bio",""),
            avatar_url=serializer.validated_data.get("avatar_url",""),
        )
        user.set_password(serializer.validated_data["password"])
        user.save()
        # Auto-assign mentor for students if not provided
        if user.role == "student" and not user.mentor:
            qs = User.objects.filter(role="teacher")
            mentor = qs.filter(university_id=user.university_id).order_by("id").first() or qs.order_by("id").first()
            if mentor:
                user.mentor = mentor
                user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = University.objects.all().order_by("name")
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]
    search_fields = ["name","domain","city","country"]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrReadOnly]
    search_fields = ["username","display_name","email"]

class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all().order_by("start_date")
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name","track"]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("teacher").all().order_by("-created_at")
    serializer_class = CourseSerializer
    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy"]:
            return [IsTeacher()]
        return [IsAuthenticated()]
    def perform_create(self, serializer):
        teacher = self.request.user
        if teacher.role != "teacher":
            raise PermissionError("Only teachers can create courses")
        serializer.save(teacher=teacher)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user
        if user.role != "student":
            return Response({"detail":"Only students enroll in courses."}, status=400)
        if course.enrollments.count() >= course.capacity:
            return Response({"detail":"Course is full."}, status=400)
        enr, created = Enrollment.objects.get_or_create(user=user, course=course)
        return Response(EnrollmentSerializer(enr).data, status=201 if created else 200)

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == "teacher":
            return Enrollment.objects.filter(course__teacher=user).select_related("user","course")
        return Enrollment.objects.filter(user=user).select_related("user","course")
    def update(self, request, *args, **kwargs):
        if getattr(request.user, "role", "") != "teacher":
            return Response({"detail":"Only teachers can update enrollment/progress."}, status=403)
        enrollment = self.get_object()
        if enrollment.course.teacher != request.user:
            return Response({"detail":"You can only update your course enrollments."}, status=403)
        return super().update(request, *args, **kwargs)
    def partial_update(self, request, *args, **kwargs):
        if getattr(request.user, "role", "") != "teacher":
            return Response({"detail":"Only teachers can update enrollment/progress."}, status=403)
        enrollment = self.get_object()
        if enrollment.course.teacher != request.user:
            return Response({"detail":"You can only update your course enrollments."}, status=403)
        return super().partial_update(request, *args, **kwargs)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("-created_at")
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        GroupMember.objects.get_or_create(group=group, user=self.request.user, defaults={"role":"owner"})
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        group = self.get_object()
        gm = GroupMember.objects.filter(group=group, user=request.user).first()
        if not gm or gm.role not in ["owner","admin"]:
            return Response({"detail":"Only owner/admin can add members."}, status=403)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail":"user_id required"}, status=400)
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail":"User not found"}, status=404)
        member, _ = GroupMember.objects.get_or_create(group=group, user=u)
        return Response(GroupMemberSerializer(member).data, status=201)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        group = self.get_object()
        gm = GroupMember.objects.filter(group=group, user=request.user).first()
        if not gm or gm.role not in ["owner","admin"]:
            return Response({"detail":"Only owner/admin can remove members."}, status=403)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail":"user_id required"}, status=400)
        GroupMember.objects.filter(group=group, user_id=user_id).delete()
        return Response({"detail":"Removed"})

class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.select_related("group","user").all()
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related("group").all().order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.select_related("project","assignee").all().order_by("-created_at")
    serializer_class = ProjectTaskSerializer
    permission_classes = [IsAuthenticated]

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.select_related("from_user","to_user").all().order_by("-created_at")
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
    def get_queryset(self):
        user = self.request.user
        return Connection.objects.filter(Q(from_user=user)|Q(to_user=user))
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        conn = self.get_object()
        if conn.to_user != request.user:
            return Response({"detail":"Only the recipient can accept."}, status=403)
        conn.status = "accepted"
        conn.save()
        return Response(self.get_serializer(conn).data)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def decline(self, request, pk=None):
        conn = self.get_object()
        if conn.to_user != request.user:
            return Response({"detail":"Only the recipient can decline."}, status=403)
        conn.status = "declined"
        conn.save()
        return Response(self.get_serializer(conn).data)
