from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.users.models import CRMUser
from apps.utils.enums import RoleType


class IsCRMUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return hasattr(request.user, 'crm_user')


class IsAdminOrReadOnly(IsCRMUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            crm_user = request.user.crm_user
            return crm_user and (crm_user.role == RoleType.ADMIN) or request.method in SAFE_METHODS
        return False
