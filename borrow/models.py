from django.db import models
from django.conf import settings
from books.models import Book

class BorrowRecord(models.Model):
    """ Модель выдачи книги читателю и возвращения книги в библиотеку. """
    STATUS_CHOICES = [
        ('BORROWED', 'Выдана'),                 # книга у читателя
        ('RETURNED', 'Возвращена'),             # книга в библиотеке
        ('OVERDUE', 'Просрочена'),              # книгу не вернули вовремя
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')                     # какая книга
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrows') # кто взял
    borrowed_at = models.DateTimeField(auto_now_add=True)                                                # когда
    due_date = models.DateField()                                                                        # когда нужно вернуть
    returned_at = models.DateTimeField(null=True, blank=True)                                            # когда вернули (если вернули)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BORROWED')                 # текущий статус книги
    notes = models.TextField(blank=True)                                                                 # примечания

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"      # отображение в адмике (переопределено в borrow/admin.py)

    class Meta:
        ordering = ['-borrowed_at']
        indexes = [
            models.Index(fields=['status']),                # быстрый поиск по статусу книги
            models.Index(fields=['due_date']),              # быстрый поиск по срокам возврата книги
        ]