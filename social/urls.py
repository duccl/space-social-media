from django.urls import path
from .import views
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('topic/<int:id>/posts/',views.PostListView.as_view(),name='post_list'),
    path('topic/<int:id>/posts/<int:post_id>/',views.PostDetailView.as_view(),name='post_detail'),
    path('topic/<int:id>/posts/<int:post_id>/create_comment',views.CommentCreateView.as_view(),name='comment_create'),
    path('topic/<int:id>/create_post/',views.PostCreateView.as_view(),name='post_create'),
    path('topic/<int:id>/edit_post/<int:post_id>',views.PostUpdateView.as_view(),name='post_edit'),
    path('delete_comment/<int:comment_id>',views.CommentDeleteView.as_view(),name='comment_delete'),
    path('drafts/',views.DraftListView.as_view(),name='posts_draft'),
    path('edit_comment/<int:comment_id>',views.CommentUpdateView.as_view(),name='comment_edit'),
    path('delete_post/<int:post_id>',views.PostDeleteView.as_view(),name='post_delete'),
    path('topics/',views.TopicListView.as_view(),name='topics'),
    path('joinUserToTopic/<int:topic_id>',views.JoinTopic.as_view(),name='join_topic'),
    path('removeUserFromTopic/<int:topic_id>',views.LeaveTopic.as_view(),name='remove_from_topic'),
    path('newTopic/',views.TopicCreateView.as_view(),name='new_topic'),
    path('resources/',views.ResourcesView.as_view(),name='resources'),
]
