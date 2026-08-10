from django.conf import settings
from django.db import models


class Author(models.Model):
    """Модель автора книги."""

    last_name = models.CharField(
        max_length=100, verbose_name="Фамилия"
    )  # фамилия автора
    first_name = models.CharField(max_length=100, verbose_name="Имя")  # имя автора
    middle_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Отчество"
    )  # отчество автора
    bio = models.TextField(blank=True, null=True)  # биография автора
    birth_date = models.DateField(verbose_name="Дата рождения")  # дата рождения автора

    @property
    def full_name_short(self):
        """Пушкин А.С."""
        return f"{self.last_name} {self.first_name[0]}.{self.middle_name[0] if self.middle_name else ''}"

    @property
    def full_name(self):
        """Александр Сергеевич Пушкин"""
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}"

    def __str__(self):
        return self.full_name_short

    class Meta:
        ordering = [
            "last_name",
            "first_name",
            "middle_name",
        ]  # сортировка по фамилии, имени, отчеству по алфавиту


class Book(models.Model):
    """Модель книги."""

    GENRES = [
        ("FIC", "Художественная"),
        ("CLD", "Детская"),
        ("SCI", "Научная"),
        ("TEC", "Техническая"),
        ("HIS", "Историческая"),
        ("BIO", "Биография"),
        ("POE", "Поэзия"),
        ("DRA", "Драма"),
    ]

    title = models.CharField(max_length=255)  # название
    isbn = models.CharField(max_length=13, unique=True)  # идентификатор
    description = models.TextField(blank=True)  # описание
    genre = models.CharField(max_length=3, choices=GENRES)  # жанр
    year = models.PositiveIntegerField(verbose_name="Год издания")  # год издания
    pages = models.PositiveIntegerField(
        verbose_name="Количество страниц"
    )  # кол-во страниц
    authors = models.ManyToManyField(Author, related_name="books")  # авторы
    # total_copies = models.PositiveIntegerField(default=1)  # всего экземпляров
    # available_copies = models.PositiveIntegerField(default=1)  # кол-во экземпляров доступных к выдаче
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания
    updated_at = models.DateTimeField(auto_now=True)  # дата обновления

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]  # сортировка по названию книги
        indexes = [
            models.Index(fields=["title"]),  # быстрый поиск по названию
            models.Index(fields=["genre"]),  # быстрый поиск по жанру
            models.Index(fields=["year"]),  # быстрый поиск по году издания
        ]


class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="items")
    inventory_number = models.CharField(
        max_length=50, unique=True, verbose_name="Инвентарный номер"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступна для выдачи")
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто взял",
    )

    def __str__(self):
        return f"{self.book.title} (№{self.inventory_number})"
