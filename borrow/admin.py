from django.contrib import admin
from .models import BorrowRecord

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'status', 'borrowed_at', 'due_date', 'returned_at')    # какие поля показывать в списке всех записей
    list_filter = ('status', 'borrowed_at')                                                      # фильтры в правой боковой панели
    search_fields = ('user__email', 'book__title')                                               # поисковая строка сверху
