from django.db import models
from django.contrib.auth.models import Group
from django.urls import reverse
from django import template
register = template.Library()
class Topic(Group):
    description = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("social:post_list", kwargs={"id": self.pk})
    