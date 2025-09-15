from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    domain = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=80, default="Kenya")
    def __str__(self):
        return self.name

class Cohort(models.Model):
    name = models.CharField(max_length=120)
    track = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveIntegerField(default=30)
    def __str__(self):
        return f"{self.name} ({self.track})"

class User(AbstractUser):
    ROLE_CHOICES = (("student","Student"), ("teacher","Teacher"))
    display_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    university = models.ForeignKey(University, on_delete=models.PROTECT)  # required
    mentor = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="mentees")
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    is_verified_student = models.BooleanField(default=False)
    def __str__(self):
        return self.display_name or self.username

class Course(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    cohort = models.ForeignKey(Cohort, null=True, blank=True, on_delete=models.SET_NULL)
    capacity = models.PositiveIntegerField(default=40)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.teacher}"

class Enrollment(models.Model):
    STATUS_CHOICES = (("active","Active"),("completed","Completed"),("dropped","Dropped"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    progress = models.PositiveSmallIntegerField(default=0)  # 0-100
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user","course")
    def __str__(self):
        return f"{self.user} → {self.course} ({self.status}, {self.progress}%)"

class Group(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class GroupMember(models.Model):
    ROLE_CHOICES = (("owner","Owner"),("admin","Admin"),("member","Member"))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("group","user")
    def __str__(self):
        return f"{self.user} in {self.group} ({self.role})"

class Project(models.Model):
    STATUS_CHOICES = (("planning","Planning"),("active","Active"),("paused","Paused"),("completed","Completed"))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="planning")
    repo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class ProjectTask(models.Model):
    STATUS_CHOICES = (("todo","To Do"),("doing","Doing"),("done","Done"))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="todo")
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Connection(models.Model):
    STATUS = (("pending","Pending"),("accepted","Accepted"),("declined","Declined"),("blocked","Blocked"))
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("from_user","to_user")
    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"
