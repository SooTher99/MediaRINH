from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.channel.models import RoleUserChannel

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        elif user and request.user.is_authenticated:
            user_channel = obj.userschannelmodel_set.filter(user=user).first()
            if user_channel.role == RoleUserChannel.ADMIN:
                return True
            else:
                return False
        else:
            return False
