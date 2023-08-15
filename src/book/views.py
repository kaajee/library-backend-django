from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.book.models import Book
from src.book.serializers import BookSerializer, BookBorrowerSerializer
from src.iam.permissions import IsLibrarianUser


@api_view(['GET'])
def api_book_list(request):
    books = Book.objects.all()
    response_data = {'books': BookSerializer(books, many=True).data}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_book_detail(request, book_id):
    exist_book = Book.objects.filter(id=book_id).first()
    if not exist_book:
        return Response({'message': 'Book is not registered'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(BookSerializer(exist_book).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLibrarianUser, ])
def api_book_borrower(request, book_id):
    exist_book = Book.objects.filter(id=book_id).first()
    if not exist_book:
        return Response({'message': 'Book is not registered'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(BookBorrowerSerializer(exist_book).data, status=status.HTTP_200_OK)
