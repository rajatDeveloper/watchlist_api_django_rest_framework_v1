from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            admin_permission = bool(request.user and request.user.is_staff)
            return admin_permission
        
        
        
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #both things are same things 
        # if request.method == "GET":
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # return obj.review_user == request.user or request.user.is_staff
            return obj.review_user == request.user or request.user.is_staff