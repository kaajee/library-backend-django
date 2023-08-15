from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APILiveServerTestCase

from src.book.factory import BookFactory
from src.borrow.factory import BorrowedBookFactory
from src.iam.factory import LibraryUserFactory


class TestBook(APILiveServerTestCase):
    def setUp(self) -> None:
        self.student = LibraryUserFactory(is_student=True, is_librarian=False)
        self.student_token = str(Token.objects.create(user=self.student.user))

        self.librarian = LibraryUserFactory(is_student=False, is_librarian=True)
        self.librarian_token = str(Token.objects.create(user=self.librarian.user))

    def test_book_list(self):
        for _ in range(5):
            BookFactory()

        response = self.client.get(reverse('api-book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('books', [])), 5)

    def test_book_detail(self):
        book = BookFactory()

        with self.subTest('Book data exist'):
            response = self.client.get(reverse('api-book-detail', kwargs={'book_id': book.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsNotNone(response.json())

        with self.subTest('Book data doesnt exist'):
            response2 = self.client.get(reverse('api-book-detail', kwargs={'book_id': 432}))
            self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_borrower(self):
        book = BookFactory()
        for _ in range(5):
            BorrowedBookFactory(book=book)

        with self.subTest('Book data exist'):
            response = self.client.get(
                reverse('api-book-borrower', kwargs={'book_id': book.id}),
                HTTP_AUTHORIZATION=f"Token {self.librarian_token}"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json().get('borrower', [])), 5)

        with self.subTest('Book data doesnt exist'):
            response2 = self.client.get(reverse('api-book-borrower', kwargs={'book_id': 432}),
                                        HTTP_AUTHORIZATION=f"Token {self.librarian_token}")
            self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
