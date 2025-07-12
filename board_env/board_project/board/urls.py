# board/urls.py

from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    # 댓글 URL
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('post/<int:pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]