from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

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
    

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    def is_valid(self):
        """Valid token for 1 hour"""
        expiry_time = self.created_at + timedelta(hours=1)
        return timezone.now() < expiry_time and not self.used
    
    def mark_as_used(self):
        """Mark as used"""
        self.used = True
        self.save()
    
    @classmethod
    def cleanup_expired_token(cls):
        """Remove expired tokens"""
        expiry_time = timezone.now() - timedelta(hours=1)
        cls.objects.filter(created_at__lt=expiry_time).delete()

