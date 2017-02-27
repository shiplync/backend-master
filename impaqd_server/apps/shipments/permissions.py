from rest_framework import permissions
from rest_framework.permissions import (
    DjangoModelPermissions, DjangoObjectPermissions)


class AccessBlockType(object):
    UNKNOWN = 'unknown'
    UNVERIFIED = 'unverified'
    PENDING_REGISTRATION = 'pendingregistration'
    TRIAL_EXPIRED = 'trialexpired'

    CHOICES = (
        (UNKNOWN, 'Unknown'),
        (UNVERIFIED, 'Unverified'),
        (PENDING_REGISTRATION, 'Pending Registration'),
        (TRIAL_EXPIRED, 'Trial expired')
    )


class AccessBlockChecker(permissions.BasePermission):
    """
    Check if users request can proceed or should be blocked
    """
    message = AccessBlockType.UNKNOWN

    def has_permission(self, request, view):
        try:
            user = request.user.genericuser
            if not user.company.verified:
                self.message = AccessBlockType.UNVERIFIED
                return False
            elif not user.company.registration_complete:
                self.message = AccessBlockType.PENDING_REGISTRATION
                return False
            elif (not user.company.subscription.payment_ready and
                    not user.company.subscription.trial_active):
                self.message = AccessBlockType.TRIAL_EXPIRED
                return False
            return True
        except Exception:
            return False


class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
