from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    DeleteComment,
                    PostLike,
                    home
                    )
from . import views


urlpatterns = [
    path('', views.about,name='blog-home'),
    path('home/',views.home,name='blog-home'),
    path('user/<str:username>',UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post-like/<int:pk>', views.PostLike, name="post_like"),
    path('about/', views.about, name='blog-about'),
    path('<comment_id>/delete/', views.DeleteComment, name='delete-comment'),
    
  
]
