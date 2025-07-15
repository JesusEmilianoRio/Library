from django.contrib import admin
from .models import Author, Category, Format, Language, Publisher, Book
# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Format)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Book)

