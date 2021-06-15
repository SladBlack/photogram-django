from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.UsersList.as_view(), name='user_list'),
    path('user_delete/<int:pk>/', views.DeleteUser.as_view(), name='user_delete'),
    path('user_block/<int:pk>/', views.BlockUser.as_view(), name='user_block'),
    path('user_create/', views.CreateUser.as_view(), name='user_create'),
]