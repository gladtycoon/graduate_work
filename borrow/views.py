from django.utils import timezone
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import BorrowRecord
from .serializers import BorrowCreateSerializer, BorrowRecordSerializer


class BorrowViewSet(viewsets.ModelViewSet):
    """Контроллер для управления выдачей книг."""

    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Обычный пользователь видит только свои выдачи, библиотекарь — все."""
        user = self.request.user
        if user.is_anonymous:
            return BorrowRecord.objects.none()
        if user.is_staff or getattr(user, "is_librarian", False):
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.filter(user=user)

    def get_serializer_class(self):
        """Для создания используем упрощенный сериализатор, для чтения — полный."""
        if self.action == "create":
            return BorrowCreateSerializer
        return BorrowRecordSerializer

    def perform_create(self, serializer):
        """Логика выдачи книги: проверка наличия и уменьшение копий."""
        book = serializer.validated_data["book"]

        # Проверяем, есть ли свободные экземпляры
        if book.available_copies < 1:
            raise serializers.ValidationError("Нет доступных копий")

        # Создаем запись о выдаче (user подставляется из токена, статус сразу BORROWED)
        serializer.save(user=self.request.user, status="BORROWED")

        # Уменьшаем количество доступных книг
        book.available_copies -= 1
        book.save()

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        """Кастомный эндпоинт для возврата книги."""
        borrow = self.get_object()

        # Проверяем, не возвращена ли книга уже
        if borrow.status == "RETURNED":
            return Response(
                {"error": "Книга уже возвращена"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Обновляем запись о выдаче
        borrow.returned_at = timezone.now()
        borrow.status = "RETURNED"
        borrow.save()

        # Увеличиваем количество доступных книг
        book = borrow.book
        book.available_copies += 1
        book.save()
        return Response({"message": "Книга возвращена"})
