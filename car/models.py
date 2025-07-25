from django.db import models
from accounts.models import User
from catalog.models import Book
from django.core.validators import MinValueValidator

class Car(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Carro de {self.user.username}'

class CarItem(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('car', 'book')  # Un mismo libro no puede repetirse en el mismo carro

    def __str__(self):
        return f'{self.car.user.username}'
