from django.urls import path
from .import views
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('topic/<int:id>/posts/',views.PostListView.as_view(),name='post_list'),
    path('posts/<int:id>/',views.PostDetailView.as_view(),name='post_detail'),
]
