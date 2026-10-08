from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit movies
    """

    def has_permission(self, request, view):
        #Gives access to all safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        #Only allows unsafe methods if user is staff
        return request.user.is_staff