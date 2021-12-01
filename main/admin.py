from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MeetUrl,User,Timings,Class
# Register your models here.

admin.site.register(MeetUrl)
admin.site.register(User,UserAdmin)
admin.site.register(Timings)
admin.site.register(Class)