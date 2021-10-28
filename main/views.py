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
    return render(request,'main/profile.html',{ 'data' : user })

def editor(request):
    return render(request, template_name='main/index.html')

def getMeetUrl(request,name):
    print(name)
    try:
        urlobj = Class.objects.get(classname=name)
        url = urlobj.url 
        return JsonResponse({'result':str(url) },safe=False,status=200)
    except:
        url = 'not found'    
    return JsonResponse({'result':str(url) },safe=False,status=404)



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

def createMeetUrl(request):
    
    if request.method == 'POST':
        form = MeetUrlModelForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['classname']
            form.save()
            print("saved")
            # classname = Class.objects.get(classname=name)
            # user  = User.objects.get(email=request.user.email)
            # owner = Owner.objects.create(user=user,classname=classname)
                
            
            
            # except:
            #     return render(request, 'main/create.html', {'form': form })  
           
            
        return render(request, 'main/create.html', {'form': form })    
    else:
        form = MeetUrlModelForm()           
    return render(request, 'main/create.html', {'form': form })

@csrf_exempt
def setMeetUrl(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body['email']
        classname = body['classname']
        url = body['url']
        classn = get_object_or_404(Class,classname = classname)
        user = get_object_or_404(User,email=email)
        isOwner = user.classname.filter(classname__exact=classn).exists()
        if not isOwner:
            return JsonResponse({'result': "You don't have access" },safe=False)
        classn.url = url
        classn.save()
        return JsonResponse({'result': "Updated successfully" },safe=False)

   
                    
    return JsonResponse({'result':'Method not allowed' },safe=False)

@csrf_exempt
def checkUser(request,email):
    user = get_object_or_404(User,email=email)
    if(user.is_staff):
        classes = list(user.classname.values('classname','url'))
        print(classes)
    
        return JsonResponse({'result':user.is_staff , 'data':classes },safe=False)
    return JsonResponse({'result':user.is_staff},safe=False)    
