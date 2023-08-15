from rest_framework import serializers

from src.borrow.models import BorrowedBook
from src.borrow.serializers import BorrowDetailSerializer
from src.iam.models import LibraryUser


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    books = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LibraryUser
        fields = ['username', 'books']

    def get_username(self, instance):
        return instance.user.username

    def get_books(self, instance):
        borrowed_books = BorrowedBook.objects.filter(user=instance.user).all()
        return BorrowDetailSerializer(borrowed_books, many=True).data
