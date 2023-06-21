from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """Пермишены для вьюсетов CustomUser."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.is_admin
            )


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser
                )


class TitlesGenresCategoriesPermission(permissions.BasePermission):
    """Пермишены для вьюсетов моделей Category, Genre, Title."""
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user.is_admin or request.user.is_superuser)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )
