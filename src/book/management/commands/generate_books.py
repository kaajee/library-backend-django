from django.core.management import BaseCommand

from src.book.management.fixtures.books import create_books


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_books()
