from django.db import models
from django.contrib.auth.models import User,Group
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    topic = models.OneToOneField(Group,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    content = models.TextField()

    def get_absolute_url(self):
        return reverse("social:detail", kwargs={"id": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_author')
    comment_created_date = models.DateTimeField(auto_now=True)
    comment_content = models.TextField()

    def get_absolute_url(self):
        return reverse("social:detail", kwargs={"id": self.post.pk})
    