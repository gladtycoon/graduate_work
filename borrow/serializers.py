from rest_framework import serializers

from books.serializers import BookSerializer
from users.serializers import UserSerializer

from .models import BorrowRecord


class BorrowRecordSerializer(serializers.ModelSerializer):
    """Сериализатор данных о выдаче книги"""

    book_details = BookSerializer(source="book", read_only=True)
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "book",
            "user",
            "book_details",
            "user_details",
            "borrowed_at",
            "due_date",
            "returned_at",
            "status",
            "notes",
        ]
        read_only_fields = ["borrowed_at", "status"]


class BorrowCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания новой записи о выдаче книги."""

    class Meta:
        model = BorrowRecord
        fields = ["book", "due_date", "notes"]
