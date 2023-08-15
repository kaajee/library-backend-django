import factory
from django.contrib.auth import get_user_model
from factory import SubFactory

from src.iam.models import LibraryUser


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = get_user_model()


class LibraryUserFactory(factory.django.DjangoModelFactory):
    user = SubFactory(UserFactory)
    is_student = True
    is_librarian = False

    class Meta:
        model = LibraryUser
