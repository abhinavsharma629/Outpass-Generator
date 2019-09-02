from django.contrib import admin
from .models import outPass, RegisteredColleges, Student, Requests

admin.site.register(outPass)
admin.site.register(Student)
admin.site.register(RegisteredColleges)
admin.site.register(Requests)