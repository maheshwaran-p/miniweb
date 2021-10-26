from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.editor),
    path('url/<str:name>',views.getMeetUrl),
    path('url',views.createMeetUrl),
    path('url/<str:email>/<str:classname>',views.setMeetUrl),
    path('user/<str:email>',views.checkUser)

]
