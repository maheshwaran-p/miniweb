from django.contrib import admin
from .models import MeetUrl,User,Timings,Class
# Register your models here.

admin.site.register(MeetUrl)
admin.site.register(User)
admin.site.register(Timings)
admin.site.register(Class)