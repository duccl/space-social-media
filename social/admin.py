from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    fields = ['topic','author',
              'is_published','content','title']
    search_fields = ['title']

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)