from rest_framework.permissions import IsAuthenticated


class NotAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not super(NotAuthenticated, self).has_permission(request, view)
