from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.editor),
    path('profile',views.Profile),
    path('url/<str:name>',views.getMeetUrl),
    path('url',views.createMeetUrl),
    path('seturl/',views.setMeetUrl),
    path('user/<str:email>',views.checkUser)

]
