from django.urls import path, include
from django.contrib import admin
from . import views,staffview



staffpattern = [
    path('profile',staffview.Profile),
    path('createclass',staffview.ClassCreateView.as_view(),name="createclass"),
    path('updateclass/<int:pk>',staffview.ClassUpdateView.as_view(),name="updateclass"),

]




studentpattern = [
    path('camera', views.editor),
   
    path('url/<str:name>',views.getMeetUrl),
    
    path('seturl/',views.setMeetUrl),
    path('user/<str:email>',views.checkUser)

]

urlpatterns = studentpattern +staffpattern

