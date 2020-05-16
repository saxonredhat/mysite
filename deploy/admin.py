from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Repository)
admin.site.register(Job)
admin.site.register(JobPlan)
admin.site.register(JenkinsJob)