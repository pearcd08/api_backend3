from rest_framework import permissions


class IsLecturer(permissions.BasePermission):
    message = "You are not a Lecturer"

    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list("name", flat=True)
        if "Lecturer" in user_groups:
            return True
        return False


class IsStudent(permissions.BasePermission):
    message = "You are not a Student"

    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list("name", flat=True)
        if "Student" in user_groups:
            return True
        return False
