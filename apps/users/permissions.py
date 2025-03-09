from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission

from apps.users.models import CRMUser
from apps.utils.enums import RoleType


class IsCRMUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return hasattr(request.user, 'crm_user')


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.method in SAFE_METHODS


class IsAdmin(IsCRMUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            user = request.user
            crm_user = getattr(user, 'crm_user', None)
            return crm_user and (crm_user.role == RoleType.ADMIN)
        return False


class IsManager(IsCRMUser):
    message = 'У вас нет разрешения для выполнения этого действия.'

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            user = request.user
            crm_user = getattr(user, 'crm_user', None)
            return crm_user and (crm_user.role == RoleType.MANAGER)
        return False


class IsClientUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return hasattr(request.user, 'client_user') and request.user.client_user.is_email_valid
