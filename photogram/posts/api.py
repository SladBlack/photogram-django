from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

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
        for item in self.request.FILES.getlist('image'):
            Post.objects.create(image=item, author=self.request.user, tag=self.request.tag)
