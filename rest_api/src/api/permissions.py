from rest_framework.permissions import BasePermission

class IsSchoolboy(BasePermission):
    def has_permission(self, request, view):
        return bool((not request.user.is_staff and request.user.is_authenticated))

class SchoolboyLoginRequired():
    permission_classes = [IsSchoolboy]

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff and request.user.is_authenticated)

class TeacherLoginRequired():
    permission_classes = [IsTeacher]