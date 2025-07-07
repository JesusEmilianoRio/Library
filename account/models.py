from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['pk',]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.pk} - {self.username}"
    
