from django.contrib.auth.models import User
from django.db import models

from src.book.models import Book


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    renewed = models.BooleanField(default=False)


class Renewal(models.Model):
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE)
    renewal_date = models.DateField()
    renewal_count = models.PositiveIntegerField(default=0)