from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "is_librarian",
        "is_staff",
        "is_active",
    )  # какие поля показывать в списке всех записей
    list_filter = ("is_librarian", "is_staff", "is_active")  # фильтр справа
    search_fields = ("email", "username", "phone")  # поиск вверху
    fieldsets = UserAdmin.fieldsets + (  # группировка полей на странице редактирования
        (
            "Дополнительные поля",
            {  # (разбивает длинную форму на логические блоки с заголовками)
                "fields": ("phone", "address", "birth_date", "is_librarian")
            },
        ),
    )
