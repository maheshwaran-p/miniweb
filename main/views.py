from django.shortcuts import render,get_object_or_404
from .models import Class,User,MeetUrl,Timings
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


# def createMeetUrl(request):
    
#     if request.method == 'POST':
#         form = MeetUrlModelForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['classname']
#             form.save()
#             print("saved")
#             # classname = Class.objects.get(classname=name)
#             # user  = User.objects.get(email=request.user.email)
#             # owner = Owner.objects.create(user=user,classname=classname)
                
            
            
#             # except:
#             #     return render(request, 'main/create.html', {'form': form })  
           
            
#         return render(request, 'main/create.html', {'form': form })    
#     else:
#         form = MeetUrlModelForm()           
#     return render(request, 'main/create.html', {'form': form })
from django.utils import timezone
@csrf_exempt
def setMeetUrl(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body['email']
        classname = body['classname']
        url = body['url']
        classn = get_object_or_404(Class,classname = classname)
        meet = MeetUrl.objects.get(classname=classn)
        user = get_object_or_404(User,email=email)
        isOwner = Class.objects.filter(owner__exact=user).exists()
        if not isOwner:
            return JsonResponse({'result': "You don't have access" },safe=False)
        meet.url = url
        meet.starttime = timezone.now()
        meet.save()
        print(meet.starttime,meet.created)
        return JsonResponse({'result': "Updated successfully" },safe=False)
    return JsonResponse({'result':'Method not allowed' },safe=False)

@csrf_exempt
def UnsetMeetUrl(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body['email']
        classname = body['classname']
        url = body['url']
        classn = get_object_or_404(Class,classname = classname)
        Meet = MeetUrl.objects.get(classname=classname)
        user = get_object_or_404(User,email=email)
        isOwner = Class.objects.filter(owner__exact=user).exists()
        if not isOwner:
            return JsonResponse({'result': "You don't have access" },safe=False)
        meet.url = url
        meet.endtime = timezone.now()
        meet.save()
        return JsonResponse({'result': "Updated successfully" },safe=False)
    return JsonResponse({'result':'Method not allowed' },safe=False)  


@csrf_exempt
def checkUser(request,email):
    try:
        user = User.objects.get(email=email)
    except:
        return JsonResponse({'status':404,'result':' Please create an account '},safe=False)

    if(user.is_staff):
        classes = list(Class.objects.filter(owner__exact=user).values('classname','description'))
    
        
    else:
        classes = list(Class.objects.filter(user__exact=user).values('classname','description') )    
    return JsonResponse({'status':200,'result':user.is_staff , 'data':classes },safe=False)   


@csrf_exempt
def PostTiming(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body['email']
        classname = body['classname']
        time = body['time']
        if time < 0:
            return JsonResponse({'status':200,'result':'Value should not be in negative' },safe=False)
        classn = get_object_or_404(Class,classname = classname)
        user = get_object_or_404(User,email=email)
        meet = MeetUrl.objects.filter(classname__exact=classn).order_by('-created').first()
        if meet.endtime != None:
            difference = timezone.now() - meet.endtime 
    
            toBeAdded = True if difference.seconds <= 6000  else  False
            
        else:
            toBeAdded = True 

               
        if toBeAdded:
            timings,isCreated = Timings.objects.get_or_create(classname=classn,student=user)
            if timings.timeListened != None :
                timings.timeListened = time + timings.timeListened
            else:
                timings.timeListened = time    

            timings.save()
            return JsonResponse({'status':200,'result':'updated' },safe=False)   
        else:
            return JsonResponse({'status':200,'result':'Sorry out of time' },safe=False)
         
    else:
        return JsonResponse({'status':404,'result':'Method not allowed' },safe=False)    


        




def AllClasses(request,classname):
    classe = Class.objects.get(classname=classname)
    if classe.owner == request.user:
        classes = MeetUrl.objects.filter(classname__exact=classe).order_by('-endtime')
        print(classes)
    else :
        return JsonResponse('You have no access',safe=False)    
    return render(request,'main/dashboard.html',{ 'data' : classes , 'classname' : classe })


def CalculateTime(request,pk):
    classes = MeetUrl.objects.get(pk=pk)
    print(classes)
    if  classes.endtime == 'None' or classes.endtime == None or classes.endtime == '' :
        classe = Timings.objects.filter(classname__exact=classes.classname).order_by('-timeListened')
    else:
        print(classes.starttime)
        classe = Timings.objects.filter(classname__exact=classes.classname).order_by('-timeListened')

    print(classe)
    return render(request,'main/studentdetails.html',{ 'classname': classes.classname  ,'pk' : pk , 'students' : classe })    

def population_chart(request,pk):
    labels = []
    data = []
    classes = MeetUrl.objects.get(pk=pk)
  
    if classes.endtime == 'None' or classes.endtime == None or classes.endtime == '' :
        classe = Timings.objects.filter(classname__exact=classes.classname).order_by('-timeListened')
    else:
        classe = Timings.objects.filter(classname__exact=classes.classname).order_by('-timeListened')
    for entry in classe:
        labels.append(entry.student.username)
        data.append(entry.timeListened)        
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })