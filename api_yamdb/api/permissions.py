from rest_framework.permissions import (
    BasePermission, SAFE_METHODS)

from reviews.models import UserRole


class AdminAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == UserRole.ADMIN
        )


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True


class MeUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user or request.user.is_authenticated
        )


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class AdminModeratorAuthorPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == UserRole.MODERATOR
            or request.user.role == UserRole.ADMIN
        )
