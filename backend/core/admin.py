from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model
from .models import University, Cohort, Course, Enrollment, Group, GroupMember, Project, ProjectTask, Connection

User = get_user_model()

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Profile", {"fields": ("display_name","role","university","mentor","year_of_study","bio","avatar_url","is_verified_student")}),
    )
    list_display = ("username","email","display_name","role","university","mentor","year_of_study","is_verified_student")
    search_fields = ("username","email","display_name")

admin.site.register(University)
admin.site.register(Cohort)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Project)
admin.site.register(ProjectTask)
admin.site.register(Connection)
