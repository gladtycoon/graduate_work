from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """ Кастомная модель пользователя. """
    email = models.EmailField(unique=True)                              # уникальный email юзера
    phone = models.CharField(max_length=20, blank=True, null=True)      # телефон
    address = models.TextField(blank=True)                              # адрес
    birth_date = models.DateField(null=True, blank=True)                # дата рождения
    is_librarian = models.BooleanField(default=False)                   # библиотекарь или обычный читатель

    USERNAME_FIELD = 'email'                                            # вход по email
    REQUIRED_FIELDS = ['username']

    def __str__(self):                                                 # в админке показывать email
        return self.email

    class Meta:
        ordering = ['email']                                           # сортировка по email