from datetime import datetime, timedelta

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.book.models import Book
from src.borrow.models import BorrowedBook, Renewal
from src.borrow.serializers import BorrowSerializer, RenewSerializer, RenewalDetailSerializer, BorrowDetailSerializer, \
    ReturnSerializer
from src.iam.permissions import IsLibrarianUser, IsStudentUser


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsLibrarianUser, ])
def api_borrow_book(request):
    serializer = BorrowSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    valid_data = serializer.validated_data

    for book_id in valid_data.get('books', []):
        # Get User & Book data
        book_data = Book.objects.get(id=book_id)

        # Create BorrowedBook record
        BorrowedBook.objects.create(
            user=request.user,
            book=book_data,
            due_date=datetime.now() + timedelta(days=30)
        )

    return Response({'message': 'Success borrow book'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudentUser, ])
def api_renew_book(request):
    serializer = RenewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    valid_data = serializer.validated_data

    # Get borrow data
    borrow_data = BorrowedBook.objects.filter(book_id=valid_data.get('book_id'), returned_date__isnull=True).first()
    if borrow_data is not None and borrow_data.renewed is False:
        borrow_data.renewed = True
        borrow_data.due_date = borrow_data.due_date + timedelta(days=30)
        borrow_data.save()

    Renewal.objects.create(
        borrowed_book=borrow_data,
        renewal_date=datetime.now()
    )

    return Response(BorrowDetailSerializer(borrow_data).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsLibrarianUser])
def api_return_book(request):
    serializer = ReturnSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    valid_data = serializer.validated_data

    for book_id in valid_data.get('books', []):
        user = User.objects.get(username=valid_data.get('username'))
        borrow_data = BorrowedBook.objects.filter(user=user, book_id=book_id, returned_date__isnull=True).first()
        borrow_data.returned_date = datetime.now()
        borrow_data.save()

    return Response({'message': 'Success return books'}, status=status.HTTP_200_OK)
