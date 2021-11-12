
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('privacy-policy', TemplateView.as_view(template_name='main/privacy-policy.html'))

]
