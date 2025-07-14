from django.db import models

# Create your models here.
class Book(models.Model):
    ACTIVE = 'A'
    INACTIVE = 'F'

    STATUS_CHOICE = [
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'OUT_OF_STOCK'),
    ]

    #Test before migrate
    book_title = models.CharField(max_length=200)
    book_synopsis = models.TextField()
    book_number_pages = models.IntegerField()
    book_published = models.DateField()
    book_ISBN = models.CharField(max_length=13)
    book_sku = models.CharField(max_length=12)
    book_image = models.ImageField()
    book_description = models.TextField()
    book_price = models.IntegerField()
    book_stock_quantity = models.IntegerField()
    book_status = models.CharField(max_length=1,
                                   choices=STATUS_CHOICE,
                                   default=ACTIVE)


    def __str__(self):
        return self.book_title