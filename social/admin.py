from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    fields = ['topic','author',
              'is_published','content','title']
    search_fields = ['title']
    list_filter = ['is_published']
    list_display = ['author','is_published','created_date']

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)