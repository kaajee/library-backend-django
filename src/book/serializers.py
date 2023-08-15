from django.contrib.auth.models import User
from rest_framework import serializers

from src.book.models import Book
from src.borrow.models import BorrowedBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'available_copies']


class BookBorrowerSerializer(serializers.ModelSerializer):
    borrower = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'borrower']

    def get_borrower(self, instance):
        user_list = []
        borrower_list = BorrowedBook.objects.filter(book=instance).values('user', 'borrowed_date', 'due_date',
                                                                          'returned_date')

        for borrower in borrower_list:
            library_user = User.objects.filter(id=borrower.get('user')).first()
            borrower['user'] = library_user.username
            user_list.append(borrower)
        return user_list
