from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from posts.models import Post
# Create your models here.

class CommentManager(models.Manager):
    def all(self):
        return super(CommentManager,self).filter(parent=None)

class Comment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    post=models.ForeignKey(Post)
    content=models.TextField()
    read_time=models.FloatField(null=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-timestamp']

    objects=CommentManager()

    def __str__(self):
        return self.user.username

    def children(self):
        return Comment.objects.filter(parent=self)