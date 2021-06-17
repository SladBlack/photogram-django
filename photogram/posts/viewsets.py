from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Post
from .serializers import (PostsListSerializer,
                          PostCreateSerializer,
                          UserListSerializer,
                          UserUpdateSerializer,
                          UserCreateSerializer)
from .premissions import IsAuthorEntry


class PostModelView(viewsets.ModelViewSet):
    """Просмотр/Создание/Редактирование/Удаление поста"""
    parser_classes = (MultiPartParser, FormParser,)
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        for item in self.request.FILES.getlist('image'):
            Post.objects.create(image=item, author=self.request.user, tag=self.request.POST.get('tag'))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        current_count_view = Post.objects.get(pk=kwargs.get('pk')).view_count
        Post.objects.filter(pk=kwargs.get('pk')).update(view_count=current_count_view + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAuthorEntry]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        else:
            return PostsListSerializer


class UserModelView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        else:
            return UserListSerializer

