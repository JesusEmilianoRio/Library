from django.db import models
from accounts.models import User
from catalog.models import Book
from django.core.validators import MinValueValidator

# Create your models here.

class UserPayment(models.Model):
    STATUS_CHOICES = [
         ('pending', 'Pending'),
         ('paid',    'Paid'),
         ('failed',  'Failed'),
     ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_session_id  = models.CharField(max_length=255, unique=True)
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="ID Stripe Product"
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID del precio en Stripe (optional)"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, 
                                decimal_places=2,
                                validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3)
    has_paid = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.book.book_title} - Paid: {self.has_paid}'