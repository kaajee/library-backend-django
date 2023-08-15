import factory

from src.book.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('name')
    author = factory.Faker('name')
    total_copies = 1
    available_copies = 1

    class Meta:
        model = Book