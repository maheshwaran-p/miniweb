from django.shortcuts import render,get_object_or_404
from .models import MeetUrl,User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

import json



def editor(request):
    return render(request, template_name='main/index.html')

def getMeetUrl(request,name):
    print(name)
    try:
        urlobj = MeetUrl.objects.get(classname=name)
        url = urlobj.url 
        return JsonResponse({'result':str(url) },safe=False,status=200)
    except:
        url = 'not found'    
    return JsonResponse({'result':str(url) },safe=False,status=404)
@csrf_exempt
def createMeetUrl(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        classname = body['classname']
        url = body['url']
        print(classname,url)
        try:
            object,isCreated = MeetUrl.objects.update_or_create(classname=classname,url=url)
            return JsonResponse({'result':'success' },safe=False)
        except:
            return JsonResponse({'result':'error' },safe=False)    
    return JsonResponse({'result':'Method not allowed' },safe=False)

@csrf_exempt
def setMeetUrl(request,email,classname):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body['email']
        classname = body['classname']
        url = body['url']
        classn = get_object_or_404(MeetUrl,classname = classname)
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
