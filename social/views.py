from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404,get_list_or_404
from django.views.generic import ListView,CreateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from . import models
from django.contrib.auth.models import Group,User
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect

class HomeView(TemplateView):
    template_name = 'social/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context

class CommentCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.Comment
    template_name = "social/comment_create.html"
    permission_required = ('social.add_comment')
    fields = ('comment_content',)

    def form_valid(self, form):
        user = get_object_or_404(User,pk=self.request.user.pk)
        post = get_object_or_404(models.Post,id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.comment_author =user
        comment.post = post
        comment.save()
        return HttpResponseRedirect(reverse('social:post_detail',kwargs={'id':self.kwargs['id'],'post_id':post.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New comment"
        return context
    
    


class PostDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required = ('social.view_post')
    model = models.Post
    template_name = "social/post_detail.html"
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = models.Comment.objects.filter(post=self.get_object())
        context['topic_id'] = self.kwargs['id']
        context["title"] = self.get_object().title
        return context
    
class PostCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.Post
    template_name = "social/post_create.html"
    permission_required = ('social.add_post')
    fields = ('title','content')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Post"
        return context
    
    def form_valid(self, form):
        topic = get_object_or_404(Group,pk = self.kwargs['id'])
        user = get_object_or_404(User,pk = self.request.user.pk)
        post = form.save(commit=False)
        post.author = user
        post.topic = topic
        post.save()
        return HttpResponseRedirect(reverse('social:post_detail',kwargs={'id':self.kwargs['id'],'post_id':post.id}))


class PostDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.Post
    template_name = "social/post_delete.html"
    permission_required=('social.delete_post')
    slug_field = 'id'
    slug_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('accounts:profile',kwargs={'id':self.request.user.pk})

class PostListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.Post
    template_name = "social/post_list.html"
    permission_required = ('social.view_post')
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic_id'] = self.kwargs['id']
        return context
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        topic = get_object_or_404(Group,pk=self.kwargs['id'])
        return models.Post.objects.filter(topic=topic,is_published=True)
