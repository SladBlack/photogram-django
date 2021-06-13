from django.conf.urls import url
from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete'),
]
