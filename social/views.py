from django.shortcuts import render
from django.views.generic.base import TemplateView,RedirectView
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, CreateView, DeleteView,RedirectView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from django.contrib.auth.models import User, Permission
from accounts.models import *
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


login_url = 'accounts:login'

class JoinTopic(LoginRequiredMixin,RedirectView):
    login_url = login_url

    def get_redirect_url(self, *args, **kwargs):
        return reverse("social:topics")
    
    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic,pk=kwargs.get('topic_id'))
        user = get_object_or_404(User,pk=request.user.pk)
        if not user.groups.filter(name = topic.name).exists():
            topic.user_set.add(user)
            messages.success(self.request,f"You joined {topic.name}!")
        else:
            messages.warning(self.request,f"You already joined {topic.name}!")
        return super().get(request, *args, **kwargs)

class LeaveTopic(LoginRequiredMixin,RedirectView):
    login_url = login_url
    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:profile",kwargs={'id':self.request.user.pk})
    
    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic,pk=kwargs.get('topic_id'))
        user = get_object_or_404(User,pk=request.user.pk)
        if user.groups.filter(name = topic.name).exists():
            topic.user_set.remove(user)
            messages.success(self.request,f"You leaved {topic.name}!")
        else:
            messages.warning(self.request,f"You are not in this {topic.name}!")
        return super().get(request, *args, **kwargs)

class TopicCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Topic
    permission_required = ('accounts.add_topic')
    template_name = "social/topic_create.html"
    fields = ('name','description')
    login_url = login_url
    def form_valid(self,form):
        topic = form.save()
        social_permissions = Permission.objects.filter(content_type__app_label='social').values('id')
        topic.permissions.add(social_permissions)
        topic.save()
        return HttpResponseRedirect(reverse('social:post_list',kwargs={'id':topic.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Topic"
        return context
    


class HomeView(TemplateView):
    template_name = 'social/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context

class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Comment
    template_name = "social/comment_create.html"
    permission_required = ('social.add_comment')
    fields = ('comment_content',)
    login_url = login_url
    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.request.user.pk)
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.comment_author = user
        comment.post = post
        comment.save()
        return HttpResponseRedirect(reverse('social:post_detail', kwargs={'id': self.kwargs['id'], 'post_id': post.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New comment"
        return context


class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = "social/comment_delete.html"
    permission_required = ('social.delete_comment')
    slug_field = 'id'
    slug_url_kwarg = 'comment_id'
    login_url = login_url
    def get_success_url(self):
        return reverse_lazy('social:post_detail', kwargs={'id': self.get_object().post.topic.pk, 'post_id': self.get_object().post.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Comment"
        return context


class CommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = "social/comment_update.html"
    permission_required = ('social.change_comment')
    slug_field = 'id'
    slug_url_kwarg = 'comment_id'
    fields = ('comment_content',)
    login_url = login_url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Comment"
        return context

    def get_success_url(self):
        return reverse_lazy('social:post_detail', kwargs={'id': self.get_object().post.topic.pk, 'post_id': self.get_object().post.id})

class TopicListView(LoginRequiredMixin,ListView):
    model = Topic
    template_name = 'social/topics_list.html'
    context_object_name = 'topics'
    login_url = login_url

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('social.change_post')
    model = Post
    template_name = 'social/post_edit.html'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    fields = ('title', 'content','is_published')
    login_url = login_url
    def get_success_url(self):
        return reverse('social:post_detail', kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Edit {self.get_object().title}'
        return context


class PostDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('social.view_post')
    model = Post
    template_name = "social/post_detail.html"
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    context_object_name = 'post'
    login_url = login_url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            post=self.get_object())
        context['topic_id'] = self.kwargs['id']
        context["title"] = self.get_object().title
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = "social/post_create.html"
    permission_required = ('social.add_post')
    fields = ('title', 'content')
    login_url = login_url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Post"
        return context

    def publish(self):
        return 'Publish' in self.request.POST

    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['id'])
        user = get_object_or_404(User, pk=self.request.user.pk)
        post = form.save(commit=False)
        post.author = user
        post.is_published = self.publish()
        post.topic = topic
        post.save()
        return HttpResponseRedirect(reverse('social:post_detail', kwargs={'id': self.kwargs['id'], 'post_id': post.id}))


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "social/post_delete.html"
    permission_required = ('social.delete_post')
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    login_url = login_url
    context_object_name = "post"
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'id': self.request.user.pk})
    

class DraftListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    template_name = "social/post_list.html"
    permission_required = ('social.view_post','social.change_post')
    context_object_name = 'posts'
    login_url = login_url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Drafts'
        return context

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user,is_published=False)
    

class PostListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    template_name = "social/post_list.html"
    permission_required = ('social.view_post')
    context_object_name = 'posts'
    login_url = login_url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic_id'] = self.kwargs['id']
        return context

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['id'])
        return Post.objects.filter(topic=topic, is_published=True)
