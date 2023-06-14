from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff or request.user.is_superuser
        )


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PATCH':
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
