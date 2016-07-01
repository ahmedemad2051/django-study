from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save
from .utils import get_read_time
def upload_location(instance,filename):
    return '%s/%s-%s' % ('posts',instance.id,filename)

class PostManager(models.Manager):
    def active(self):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

class Post(models.Model):
    title=models.CharField(max_length=120)
    image=models.ImageField(null=True,blank=True,upload_to=upload_location)
    content=models.TextField()
    draft=models.BooleanField(default=False)
    publish=models.DateField(auto_now=False,auto_now_add=False)
    read_time=models.TimeField(null=True,blank=True)
    update=models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)

    objects=PostManager()

    def __str__(self):
        return self.title


def pre_save_post(sender,instance,*args,**kwargs):
    if instance.content:
        read_time=get_read_time(instance.content)
        instance.read_time=read_time

pre_save.connect(pre_save_post,sender=Post)