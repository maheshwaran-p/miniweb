from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.editor),
    path('url/<str:name>',views.getMeetUrl),
    path('url',views.setMeetUrl)

]
