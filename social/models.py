from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from django.utils import timezone
from django.urls import reverse
from django import template
register = template.Library()

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='topic')
    title = models.CharField(max_length=30,blank=False)
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)
    content = models.TextField(default='')

    def get_absolute_url(self):
        return reverse("social:detail", kwargs={"id": self.pk})
    
    def __str__(self):
        return self.author.username

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    comment_author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_author')
    comment_created_date = models.DateTimeField(auto_now=True)
    comment_content = models.TextField(default='')

    def __str__(self):
        return self.comment_author.username

    def get_absolute_url(self):
        return reverse("social:detail", kwargs={"id": self.post.pk})
    