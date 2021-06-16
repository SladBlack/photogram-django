from rest_framework.permissions import BasePermission


class IsAuthorEntry(BasePermission):
    """Автор записи или админимтратор"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff
