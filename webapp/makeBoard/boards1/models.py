from django.db import models

from django.contrib.auth.models import User

class Topic(models.Model):
    message = models.TextField(max_length=5000,null=True)
    subject = models.CharField(max_length=255)
    last_updated =  models.DateField(auto_now_add=True, null=True)
    writter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.subject

class Reply(models.Model):
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by= models.ForeignKey(User, null=True, related_name='posts',on_delete=models.CASCADE)
    updated_at = models.DateField(null = True)
    updated_by =  models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)

class Answer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000,null=True)
    create_date = models.DateField()
    writter = models.ForeignKey(User, on_delete=models.CASCADE)