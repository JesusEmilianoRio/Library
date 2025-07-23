from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.utils.text import slugify
from django.urls import reverse

#Class that filters categories
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100, unique=True)

    #If not category_slug, it will create a new one with category_name
    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

#Class that defines book language
class Language(models.Model):
    language_name = models.CharField(max_length=100)

    def __str__(self):
        return self.language_name

#Class taht defines type format, such as pasta dura o pasta blanda
class Format(models.Model):
    type_format = models.CharField(max_length=100)

    def __str__(self):
        return self.type_format

#Class that defines editorial.
class Publisher(models.Model):
    publisher_name = models.CharField(max_length=200)

    def __str__(self):
        return self.publisher_name

#Class that defines who wrote the book
class Author(models.Model):
    author_first_name = models.CharField(max_length=30)
    author_last_name = models.CharField(max_length=30)
    author_bio = models.TextField()

    def __str__(self):
        return f'{self.author_first_name} {self.author_last_name}'

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
    book_image = models.ImageField(upload_to='books/')
    book_price = models.IntegerField()
    book_stock_quantity = models.IntegerField()
    book_slug = models.SlugField(max_length=200, unique=True)
    book_status = models.CharField(max_length=1,
                                   choices=STATUS_CHOICE,
                                   default=ACTIVE)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books',
    )
    category = models.ManyToManyField(
        Category,
        related_name='books',
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        related_name='books'
    )
    languages = models.ManyToManyField(
        Language,
        related_name='books',
    )
    formats = models.ManyToManyField(
        Format,
        related_name='books',
    )


    def __str__(self):
        return self.book_title
    
    
    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        #If not slug, it will create a new one with book_title
        if not self.book_slug:
            self.book_slug = slugify(self.book_title)

        if self.book_image:  # Check if an image is present
            # Open the image using Pillow
            img = Image.open(self.book_image)
            # Create a BytesIO object to save the compressed image
            img_io = BytesIO()
            # Compress the image (e.g., to JPEG with quality 60)
            # You can adjust format and quality as needed
            img.save(img_io, 'jpeg', quality=60)
            # Create a new Django File object from the compressed image data
            new_image = File(img_io, name=self.book_image.name)
            # Assign the compressed image back to the image field
            self.book_image = new_image

        super().save(*args, **kwargs) # Call the original save method