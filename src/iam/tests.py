from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APILiveServerTestCase

from src.borrow.factory import BorrowedBookFactory
from src.iam.factory import LibraryUserFactory
from src.iam.models import LibraryUser
fake = Faker()


class TestIam(APILiveServerTestCase):

    def test_register_student(self):
        username = fake.user_name()
        password = fake.password()

        with self.subTest('Success'):
            response = self.client.post(
                reverse('api-user-registration'),
                data={
                    'username': username,
                    'password': password,
                    'role': 'student'
                }
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(LibraryUser.objects.count(), 1)
            self.assertEqual(LibraryUser.objects.first().is_student, True)
            self.assertEqual(LibraryUser.objects.first().is_librarian, False)

        with self.subTest('Duplicate register'):
            response2 = self.client.post(
                reverse('api-user-registration'),
                data={
                    'username': username,
                    'password': password,
                    'role': 'student'
                }
            )
            self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_register_librarian(self):

        with self.subTest('Success'):
            response = self.client.post(
                reverse('api-user-registration'),
                data={
                    'username': fake.user_name(),
                    'password': fake.password(),
                    'role': 'librarian'
                }
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(LibraryUser.objects.count(), 1)
            self.assertEqual(LibraryUser.objects.first().is_student, False)
            self.assertEqual(LibraryUser.objects.first().is_librarian, True)

        with self.subTest('Bad Request'):
            bad_request = self.client.post(
                reverse('api-user-registration'),
                data={
                    'username': fake.user_name(),
                    'role': 'librarian'
                }
            )

            self.assertEqual(bad_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        username = fake.user_name()
        password = fake.password()

        self.client.post(
            reverse('api-user-registration'),
            data={
                'username': username,
                'password': password,
                'role': 'student'
            }
        )

        with self.subTest('Success login'):
            success_login = self.client.post(
                reverse('api-user-login'),
                data={
                    'username': username,
                    'password': password
                }
            )

            self.assertEqual(success_login.status_code, status.HTTP_200_OK)

        with self.subTest('Unauthorized'):
            unauthorized = self.client.post(
                reverse('api-user-login'),
                data={
                    'username': fake.user_name(),
                    'password': fake.password()
                }
            )

            self.assertEqual(unauthorized.status_code, status.HTTP_401_UNAUTHORIZED)

        with self.subTest('bad_request'):
            bad_request = self.client.post(
                reverse('api-user-login'),
                data={
                    'username': fake.user_name()
                }
            )

            self.assertEqual(bad_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile(self):
        student = LibraryUserFactory(is_student=True, is_librarian=False)
        token = str(Token.objects.create(user=student.user))
        for _ in range(3):
            BorrowedBookFactory(user=student.user)

        response = self.client.get(reverse('api-user-profile'), HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.json().get('books', [])
        self.assertEqual(len(books), 3)
