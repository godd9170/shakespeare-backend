from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to see it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # print("permission obj: {}".format(obj.owner.__dict__))
        # print("permission request: {}".format(request.user.__dict__))
        # print("user = owner?: {}".format(obj.owner == request.user))
        # # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
        #return False