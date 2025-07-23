from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Book


def index(request):
    return render(request, 'catalog/index.html', )

#Specific page to render a particular book.
def book_detail(request, pk):
    book = get_object_or_404(Book, pk = pk)
    other_books = Book.objects.exclude(pk=book.pk)[:4]
    return render(request, 'catalog/detail.html', { 
        "book" : book, 
        "other_books" : other_books 
    })