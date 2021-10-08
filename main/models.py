from django.db import models

# Create your models here.

class MeetUrl(models.Model):
    classname = models.CharField(max_length=15,unique=True)
    url = models.URLField()
    def __str__(self):
        return str(self.classname)