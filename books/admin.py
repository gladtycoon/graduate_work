from django.contrib import admin
from .models import Book, Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birth_date')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn', 'genre', 'year', 'total_copies', 'available_copies')    # какие поля показывать в списке всех записей
    list_filter = ('genre', 'year')                                                                # фильтр справа
    search_fields = ('title', 'isbn', 'authors__name')                                             # поиск вверху
    filter_horizontal = ('authors',)                                                               # двухколоночная панель внизу