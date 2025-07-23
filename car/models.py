from django.db import models
from accounts.models import User
from catalog.models import Book
from django.core.validators import MinValueValidator
# Create your models here.

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book)
    quantity = models.PositiveIntegerField(default=1,
                                           validators=[MinValueValidator])
    
    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.username} - {self.book.book_title} ({self.quantity})'
