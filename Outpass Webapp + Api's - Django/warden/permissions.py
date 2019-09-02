from rest_framework.permissions import BasePermission
from commonPanel.models import UserDetails
from warden.models import Warden

class WardenAccessPermissions(BasePermission):
    message = '''Can't Access Full Warden Details Or Perform Actions That Are Owned By A Verified Warden!!'''

    def has_permission(self, request, view):
        if(UserDetails.objects.get(user=request.user).type=="W" and Warden.objects.get(warden=UserDetails.objects.get(user=request.user)).isVerified==True):
            return True
        else:
            return False

class WardenAccessPermissionsWithoutVerification(BasePermission):
    message = '''Can't Access Full Warden Details Or Perform Actions That Are Owned By A Verified Warden!!'''

    def has_permission(self, request, view):
        if(UserDetails.objects.get(user=request.user).type=="W"):
            return True
        else:
            return False

class StudentAccessPermissions(BasePermission):
    message = '''A Warden Can't Access and Perform Some Actions That Are Owned By A Studen!!'''

    def has_permission(self, request, view):
        if(UserDetails.objects.get(user=request.user).type=="S"):
            return True
        else:
            return False
