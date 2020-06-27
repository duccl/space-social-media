from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404,get_list_or_404
from django.views.generic import ListView,CreateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from . import models
from django.contrib.auth.models import Group

class HomeView(TemplateView):
    template_name = 'social/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context
    
class PostDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required = ('social.view_post')
    model = models.Post
    template_name = "social/post_detail.html"
    slug_field = 'id'
    slug_url_kwarg = 'id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_object().title
        return context
    

class PostListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.Post
    template_name = "social/post_list.html"
    permission_required = ('social.view_post')
    context_object_name = 'posts'

    def get_queryset(self):
        topic = get_object_or_404(Group,pk=self.kwargs['id'])
        return get_list_or_404(models.Post,topic=topic,is_published=True)
