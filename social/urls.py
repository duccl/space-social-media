from django.urls import path
from .import views
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('topic/<int:id>/posts/',views.PostListView.as_view(),name='post_list'),
    path('topic/<int:id>/posts/<int:post_id>/',views.PostDetailView.as_view(),name='post_detail'),
    path('topic/<int:id>/posts/<int:post_id>/create_comment',views.CommentCreateView.as_view(),name='comment_create'),
    path('topic/<int:id>/create_post/',views.PostCreateView.as_view(),name='post_create'),
    path('delete_post/<int:post_id>',views.PostDeleteView.as_view(),name='post_delete'),
]
