from django.shortcuts import render
from django.urls import reverse
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

class SignUpView(CreateView):
    template_name = "accounts/home.html"
    form_class = UserCreationForm
    model = User
    success_url = ''
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:profile',kwargs={'id':request.user.pk}))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'    
    def get_success_url(self):
        return reverse('accounts:profile',kwargs={'id':self.request.user.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

class UserLogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('accounts:home'))

    

class ProfileView(LoginRequiredMixin,DetailView):
    context_object_name = 'user'
    model = User
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'accounts/profile.html'
    login_url = 'accounts:login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context['user'].username
        return context
    