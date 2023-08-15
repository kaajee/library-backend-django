from django.contrib.auth.models import User
from django.db import models

from src.borrow.models import BorrowedBook


class LibraryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
