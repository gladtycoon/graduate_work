from django.db import models


class Author(models.Model):
    """Модель автора книги."""

    name = models.CharField(max_length=255)  # имя автора
    bio = models.TextField(blank=True, null=True)  # биография автора
    birth_date = models.DateField(null=True, blank=True)  # дата рождения

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]  # сортировка по алфавиту


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
    year = models.IntegerField()  # год издания
    pages = models.IntegerField()  # кол-во страниц
    authors = models.ManyToManyField(Author, related_name="books")  # авторы
    total_copies = models.PositiveIntegerField(default=1)  # всего экземпляров
    available_copies = models.PositiveIntegerField(
        default=1
    )  # кол-во экземпляров доступных к выдаче
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
