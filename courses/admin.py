from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "capacity", "status", "owner")
    list_filter = ("status",)
    search_fields = ("title", "slug")
