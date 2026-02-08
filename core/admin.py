from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import (
    TheUser, Course, Chapter, Lesson, Enrollment
)

@admin.register(TheUser)
class TheUserAdmin(UserAdmin):
    pass
    

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Enrollment)