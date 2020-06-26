from django.urls import path
from . import views
urlpatterns = [
    path('',views.SignUpView.as_view(),name='home'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/<int:id>/',views.ProfileView.as_view(),name='profile'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
]
