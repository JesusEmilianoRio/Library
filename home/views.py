from django.shortcuts import render
from catalog.models import Book

# Create your views here.
def index(request):
    return render(request, 'home/index.html', {
        'books': Book.objects.all()  # Fetch all books from the database
    })