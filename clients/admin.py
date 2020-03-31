from django.contrib import admin
from .models import Startup, Hacker, JobApplication, JobPosition, Exchange

admin.site.register(Startup)
admin.site.register(Hacker)
admin.site.register(JobApplication)
admin.site.register(JobPosition)
admin.site.register(Exchange)
