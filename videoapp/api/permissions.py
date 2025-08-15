from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return (obj.owner == request.user) or (request.method in permissions.SAFE_METHODS)