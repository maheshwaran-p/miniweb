from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    pass

class Class(models.Model):
    classname = models.CharField(max_length=15,unique=True)
    description = models.TextField()
    owner = models.ForeignKey(User,related_name="owner",on_delete = models.CASCADE)
    user = models.ManyToManyField(User,null=True,blank=True)
    

    def __str__(self):
        return str(self.classname)




class MeetUrl(models.Model):
    classname = models.ForeignKey(Class,on_delete = models.CASCADE)
    url = models.URLField(max_length=115,null=True,blank=True)
    starttime = models.DateTimeField(null=True,blank=True)
    endtime = models.DateTimeField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.classname)



# class Owner(models.Model):
#     user = models.ForeignKey(User,on_delete = models.CASCADE) 
#     classname = models.ForeignKey(MeetUrl,on_delete = models.CASCADE)

    

class Timings(models.Model):   
    student = models.ForeignKey(User,on_delete = models.CASCADE) 
    classname = models.ForeignKey(Class,on_delete = models.CASCADE)
    timeListened  = models.FloatField(null=True,blank=True) 
    updated = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "{0} | {1} ".format(self.student,self.updated)