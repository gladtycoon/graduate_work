from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Контроллер для книг."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Точная фильтрация (?поле=значение), поиск по тексту (?search=текст), сортировка (?ordering=поле/=-поле)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["genre", "year", "authors"]
    search_fields = ["title", "isbn", "description", "authors__name"]
    ordering_fields = ["title", "year", "created_at"]

    def get_permissions(self):
        """Права доступа."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]  # для админа - все операции с книгами
        return [
            IsAuthenticated()
        ]  # для залогиненного пользователя - просмотр книги и списка книг

    # @action(detail=True, methods=["post"])
    # def borrow(self, request, pk=None):
    #     """Кастомные действия: выдача книги."""
    #     book = self.get_object()
    #     if book.available_copies < 1:
    #         return Response(
    #             {"error": "Нет доступных экземпляров"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     # Логика выдачи будет в приложении borrow
    #     return Response({"message": "Книга выдана"})
    #
    # @action(detail=True, methods=["post"])
    # def return_book(self, request, pk=None):
    #     """Кастомные действия: возврат книги."""
    #     book = self.get_object()
    #     return Response({"message": "Книга возвращена"})


class AuthorViewSet(viewsets.ModelViewSet):
    """Контроллер для автора."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # У авторов нет фильтрации по полям, только поиск и сортировка
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "bio"]  # поиск по имени и биографии
    ordering_fields = ["name", "birth_date"]  # сортировка по имени и дате рождения

    def get_permissions(self):
        """Права доступа."""
        # смотреть/искать могут все залогиненные, изменять/удалять — только админ
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
