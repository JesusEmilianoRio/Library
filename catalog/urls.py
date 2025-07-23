from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.book_detail, name='book_detail')
]
