from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Post
from .serializers import PostsListSerializer
from .premissions import IsAuthorEntry


class PostModelView(viewsets.ModelViewSet):
    """Просмотр/Создание/Редактирование/Удаление поста"""
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostsListSerializer
    permission_classes_by_action = {'update': [permissions.IsAdminUser],
                                    'destroy': [IsAuthorEntry]}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # for item in self.request.FILES.getlist('image'):
        #     Post.objects.create(image=item, author=self.request.user, tag=self.request.tag)

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