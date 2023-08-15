from rest_framework.permissions import BasePermission

from src.iam.models import LibraryUser


class IsStudentUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        library_user = LibraryUser.objects.filter(user=request.user).first()
        is_student = library_user.is_student if library_user is not None else False
        return bool(request.user and is_student)


class IsLibrarianUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        library_user = LibraryUser.objects.filter(user=request.user).first()
        is_librarian = library_user.is_librarian if library_user is not None else False
        return bool(request.user and is_librarian)