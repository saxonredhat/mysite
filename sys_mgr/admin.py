from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)

admin.site.register(Department)
admin.site.register(Position)

admin.site.register(Menu)
admin.site.register(Space)
