from rest_framework import permissions

from .models import UserRole


class IsAdminOrSuperUser(permissions.BasePermission):
    '''Права доступа для администратора'''
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.role == UserRole.ADMIN:
            return True