from rest_framework.permissions import BasePermission

class Notauthendicated(BasePermission):
    message = "zaten hesabınız var"

    def has_permission(self, request, view):
        return not request.user.is_authenticated
