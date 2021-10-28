from django.shortcuts import render,get_object_or_404
from .models import Class,User,MeetUrl
from .forms import MeetUrlModelForm

from django.http import JsonResponse,HttpResponseRedirect
from django.views.generic import CreateView,UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json


@login_required()
def Profile(request):
    
    user = User.objects.get(email=request.user.email)
    classes = Class.objects.filter(user__exact= user)

    return render(request,'main/profile.html',{ 'user' : user , 'classes' : classes })


class ClassCreateView(LoginRequiredMixin,CreateView):
    model = Class
    login_url = '/accounts/login/'
    fields = ['classname','description']
    template_name = 'main/create.html'
    success_url = '/url'
    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ClassUpdateView(LoginRequiredMixin,UpdateView):
    model = Class
    login_url = '/accounts/login/'
    fields = ['classname','description']
    template_name = 'main/create.html'
    success_url = '/url'
    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())