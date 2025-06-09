from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff