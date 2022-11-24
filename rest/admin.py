from django.contrib import admin
from rest.models import Student, Lecturer, Semester, Course, Class, CollegeDay

# Register your models here.
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(CollegeDay)