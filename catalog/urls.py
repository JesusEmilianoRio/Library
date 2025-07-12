from django.urls import path, include
from django.contrib import admin
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
]