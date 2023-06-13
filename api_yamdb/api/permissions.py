from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff or request.user.is_superuser
        )


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ['GET', 'PATCH'] and request.user.is_authenticated
        )
    #def has_object_permission(self, request, view, obj):
    #    if request.method in ['PATCH']:
    #        return obj.user == request.user
    #    return True
