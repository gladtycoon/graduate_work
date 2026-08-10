from django.contrib import admin

from .models import Author, Book, BookItem


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "middle_name", "birth_date")
    search_fields = ("last_name", "first_name", "middle_name")
    list_display_links = ("id", "last_name")  # чтобы по фамилии можно было перейти


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "isbn",
        "genre",
        "year",
        # "total_copies",
        # "available_copies",   total_copies и available_copies удалены в модели
    )  # какие поля показывать в списке всех записей
    list_filter = ("genre", "year")  # фильтр справа
    search_fields = (
        "title",
        "isbn",
        "authors__last_name",
        "authors__first_name",
    )  # поиск вверху
    filter_horizontal = ("authors",)  # двухколоночная панель внизу


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ("book", "inventory_number", "is_available", "reader")
    list_filter = ("is_available",)
    search_fields = ("inventory_number", "book__title")
