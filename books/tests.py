import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Author, Book

User = get_user_model()


class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Берём тестовые данные из переменных окружения
        test_username = os.getenv("TEST_USERNAME")
        test_email = os.getenv("TEST_EMAIL")
        test_password = os.getenv("TEST_PASSWORD")

        admin_username = os.getenv("TEST_ADMIN_USERNAME")
        admin_email = os.getenv("TEST_ADMIN_EMAIL")
        admin_password = os.getenv("TEST_ADMIN_PASSWORD")

        # Создаём обычного пользователя
        self.user = User.objects.create_user(
            username=test_username, email=test_email, password=test_password
        )

        # Создаём администратора
        self.admin = User.objects.create_superuser(
            username=admin_username, email=admin_email, password=admin_password
        )

        self.author = Author.objects.create(
            last_name="Тестов",
            first_name="Тест",
            middle_name="Тестович",
            birth_date="1990-01-01"
        )

        self.book = Book.objects.create(
            title="Test Book",
            isbn="1234567890123",
            genre="FIC",
            year=2024,
            pages=100,
            # total_copies=1,
            # available_copies=1,
        )
        self.book.authors.add(self.author)

    def test_get_books_unauthorized(self):
        """Проверяем, что без токена доступ запрещён"""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 401)

    def test_get_books_authorized(self):
        """Проверяем, что с токеном список книг доступен"""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 200)

    def test_create_book_as_admin(self):
        """Проверяем, что админ может создать книгу"""
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        data = {
            "title": "New Book",
            "isbn": "1234567890124",
            "genre": "FIC",
            "year": 2024,
            "pages": 200,
            # "total_copies": 2,
            # "available_copies": 2,
            "author_ids": [self.author.id],
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_as_user(self):
        """Проверяем, что обычный пользователь не может создать книгу"""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        data = {
            "title": "New Book",
            "isbn": "1234567890124",
            "genre": "FIC",
            "year": 2024,
            "pages": 200,
            # "total_copies": 2,
            # "available_copies": 2,
            "author_ids": [self.author.id],
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, 403)
