from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create or update roles.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the admin role
        return request.user.is_authenticated and request.user.user_type.role_name == 'Admin'


class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create or update roles.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the admin role
        return request.user.is_authenticated and request.user.user_type.role_name == 'Employer'