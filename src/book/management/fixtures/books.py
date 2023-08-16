from faker import Faker

from src.book.models import Book

fake = Faker()


def create_books():
    for _ in range(5):
        book, _ = Book.objects.get_or_create(
            title=fake.name(),
            author=fake.name(),
            total_copies=10,
            available_copies=10,
        )
        print(f' [*] Create new book {book.title}')