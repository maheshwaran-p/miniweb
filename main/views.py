from django.shortcuts import render,get_object_or_404
from .models import MeetUrl
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
def setMeetUrl(request):
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

