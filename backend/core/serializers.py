from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import University, Cohort, Course, Enrollment, Group, GroupMember, Project, ProjectTask, Connection

User = get_user_model()

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id","name","domain","city","country"]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    university = UniversitySerializer(read_only=True)
    university_id = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all(), source="university", write_only=True, required=True
    )
    mentor = serializers.SerializerMethodField(read_only=True)
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="teacher"),
        source="mentor",
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = ["id","username","email","display_name","role","bio","year_of_study","avatar_url","is_verified_student",
                  "university","university_id","mentor","mentor_id","password"]

    def get_mentor(self, obj):
        if obj.mentor:
            return {"id": obj.mentor.id, "display_name": obj.mentor.display_name or obj.mentor.username}
        return None

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ["id","name","track","description","start_date","end_date","capacity"]

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="teacher"),
        source="teacher",
        write_only=True,
        required=False
    )
    cohort = CohortSerializer(read_only=True)
    cohort_id = serializers.PrimaryKeyRelatedField(
        queryset=Cohort.objects.all(), source="cohort", write_only=True, required=False
    )
    class Meta:
        model = Course
        fields = ["id","name","description","teacher","teacher_id","cohort","cohort_id","capacity","start_date","end_date","created_at"]

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role="student"), source="user", write_only=True, required=False)
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source="course", write_only=True)
    class Meta:
        model = Enrollment
        fields = ["id","user","user_id","course","course_id","progress","status","created_at"]
        read_only_fields = ["status","created_at"]

class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source="course", write_only=True, required=False)
    class Meta:
        model = Group
        fields = ["id","name","owner","course","course_id","created_at"]

class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="user", write_only=True)
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source="group", write_only=True)
    class Meta:
        model = GroupMember
        fields = ["id","group","group_id","user","user_id","role","joined_at"]
        read_only_fields = ["joined_at"]

class ProjectSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source="group", write_only=True)
    class Meta:
        model = Project
        fields = ["id","group","group_id","name","description","status","repo_url","created_at","updated_at"]

class ProjectTaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source="project", write_only=True)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="assignee", write_only=True, required=False)
    class Meta:
        model = ProjectTask
        fields = ["id","project","project_id","title","description","status","assignee","assignee_id","due_date","created_at"]
        read_only_fields = ["created_at"]

class ConnectionSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    to_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="to_user", write_only=True)
    class Meta:
        model = Connection
        fields = ["id","from_user","to_user","to_user_id","status","created_at"]
        read_only_fields = ["status","created_at"]
