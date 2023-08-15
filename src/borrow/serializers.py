from django.contrib.auth.models import User
from rest_framework import serializers

from src.book.models import Book
from src.borrow.models import Renewal, BorrowedBook


class BorrowSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    books = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    def validate_username(self, value):
        exist_user = User.objects.filter(username=value).first()
        if not exist_user:
            raise serializers.ValidationError("Username not found")

        return value

    def validate_books(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Maximum borrowing 10 books")

        for book in value:

            exist_book = Book.objects.filter(id=book).first()

            if not exist_book:
                raise serializers.ValidationError(f"Invalid book identifier {book}, not registered")

        return value


class BorrowDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['book', 'borrowed_date', 'due_date', 'renewed']


class RenewSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)


class RenewalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renewal
        fields = ['borrowed_book', 'renewal_date']


class ReturnSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    books = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    def validate_username(self, value):
        exist_user = User.objects.filter(username=value).first()
        if not exist_user:
            raise serializers.ValidationError("Username not found")

        return value

    def validate_books(self, value):

        for book in value:
            exist_book = Book.objects.filter(id=book).first()
            if not exist_book:
                raise serializers.ValidationError(f"Invalid book identifier {book}, not registered")

            exist_borrow = BorrowedBook.objects.filter(book_id=book, returned_date__isnull=True).first()
            if not exist_borrow:
                raise serializers.ValidationError(f"Book identifier {book}, is not borrowed")

        return value
