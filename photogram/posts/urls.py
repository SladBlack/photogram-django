from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views, viewsets


urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('filter/', views.FilterView.as_view(), name='filter'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete'),
    path('my-posts/', views.MyPostsView.as_view(), name='my-posts'),
]

router = DefaultRouter()
router.register(r'posts-rest', viewsets.PostModelView, basename='post')
router.register(r'user-rest', viewsets.UserModelView, basename='user')
urlpatterns += router.urls
