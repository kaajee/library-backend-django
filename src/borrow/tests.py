from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APILiveServerTestCase

from src.book.factory import BookFactory
from src.borrow.factory import BorrowedBookFactory
from src.borrow.models import BorrowedBook, Renewal
from src.iam.factory import LibraryUserFactory

fake = Faker()


class TestBorrow(APILiveServerTestCase):
    def setUp(self) -> None:
        self.student = LibraryUserFactory(is_student=True, is_librarian=False)
        self.librarian = LibraryUserFactory(is_student=False, is_librarian=True)
        self.book = BookFactory()

        self.student_token = str(Token.objects.create(user=self.student.user))
        self.librarian_token = str(Token.objects.create(user=self.librarian.user))

    def test_borrow(self):
        response = self.client.post(
            reverse('api-borrow-book'),
            data={
                'username': self.student.user.username,
                'books': [self.book.id]
            }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BorrowedBook.objects.count(), 1)

    def test_borrow_validation(self):

        with self.subTest('Validation maximum borrowing 10 books'):
            error1 = self.client.post(
                reverse('api-borrow-book'),
                data={
                    'username': self.student.user.username,
                    'books': [self.book.id, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )

            self.assertEqual(error1.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest('Book not registered'):
            error2 = self.client.post(
                reverse('api-borrow-book'),
                data={
                    'username': self.student.user.username,
                    'books': [2123]
                }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )

            self.assertEqual(error2.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest('Username not found'):
            error3 = self.client.post(
                reverse('api-borrow-book'),
                data={
                    'username': fake.user_name(),
                    'books': [self.book.id]
                }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )

            self.assertEqual(error3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_renew(self):
        BorrowedBookFactory(book=self.book, user=self.student.user)

        response = self.client.post(
            reverse('api-renew-book'),
            data={
                'book_id': self.book.id
            }, HTTP_AUTHORIZATION=f"Token {self.student_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Renewal.objects.count(), 1)

    def test_permission(self):

        with self.subTest('Librarian Permission'):
            response_borrow = self.client.post(
                reverse('api-borrow-book'),
                data={
                    'username': self.student.user.username,
                    'books': [self.book.id]
                }, HTTP_AUTHORIZATION=f"Token {self.student_token}"
            )

            self.assertEqual(response_borrow.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest('Student Permission'):
            response_borrow = self.client.post(
                reverse('api-borrow-book'),
                data={
                    'username': self.student.user.username,
                    'books': [self.book.id]
                }, HTTP_AUTHORIZATION=f"Token {self.student_token}"
            )

            self.assertEqual(response_borrow.status_code, status.HTTP_403_FORBIDDEN)

    def test_return(self):
        BorrowedBookFactory(book=self.book, user=self.student.user)

        response = self.client.post(
            reverse('api-return-book'),
            data={
                'username': self.student.user.username,
                'books': [self.book.id]
            }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(BorrowedBook.objects.filter(book=self.book, user=self.student.user).first().returned_date)

    def test_return_validation(self):
        with self.subTest('Book not registered'):
            error1 = self.client.post(
                reverse('api-return-book'),
                data={
                    'username': self.student.user.username,
                    'books': [2123]
                }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )

            self.assertEqual(error1.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest('Book is not borrowed'):
            error1 = self.client.post(
                reverse('api-return-book'),
                data={
                    'username': self.student.user.username,
                    'books': [BookFactory().id]
                }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )

            self.assertEqual(error1.status_code, status.HTTP_400_BAD_REQUEST)

        with self.subTest('Username not found'):
            BorrowedBookFactory(book=self.book, user=self.student.user)
            error3 = self.client.post(
                reverse('api-return-book'),
                data={
                    'username': fake.user_name(),
                    'books': [self.book.id]
                }, HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )

            self.assertEqual(error3.status_code, status.HTTP_400_BAD_REQUEST)
