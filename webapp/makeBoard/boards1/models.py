from django.db import models

from django.contrib.auth.models import User

class Topic(models.Model):
    message = models.TextField(max_length=5000,null=False,blank=False)
    subject = models.CharField(max_length=255,blank=False)
    last_updated =  models.DateTimeField(auto_now_add=True, null=False,blank=False)
    writter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE, null=False,blank=False)
    view_count = models.PositiveIntegerField(default=0)

class Reply(models.Model):
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by= models.ForeignKey(User, null=True, related_name='posts',on_delete=models.CASCADE)
    updated_at = models.DateField(null = True)
    updated_by =  models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)

class Answer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000,null=False)
    create_date = models.DateTimeField(auto_now_add=True)