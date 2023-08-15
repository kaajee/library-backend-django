from datetime import datetime, timedelta

import factory
from factory import SubFactory

from src.book.factory import BookFactory
from src.borrow.models import BorrowedBook
from src.iam.factory import UserFactory


class BorrowedBookFactory(factory.django.DjangoModelFactory):
    book = SubFactory(BookFactory)
    user = SubFactory(UserFactory)
    borrowed_date = datetime.now()
    due_date = datetime.now() + timedelta(days=30)

    class Meta:
        model = BorrowedBook
