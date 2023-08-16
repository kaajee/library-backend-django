from django.core.management import BaseCommand

from src.iam.management.fixtures.users import create_users


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_users()
