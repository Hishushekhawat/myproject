from django.urls import path
from .views import ( PostListView,
                     PostDetailView,
                     PostCreateView,
                     PostUpdateView,
                     PostDeleteView,
                     UserPostListView
)

from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about,name='blog-about'),
    path('like_post/',views.like_post, name='like_post'),
    path('commentpage/<int:pk>/',views.commentpage, name='commentpage'),
    path('delete_comment/<int:pk>/',views.delete_comment,name='delete-comment')
]
