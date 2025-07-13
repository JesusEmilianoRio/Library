from django.contrib import admin
from .models import User, PasswordResetToken  # tu modelo personalizado

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'password']

admin.site.register(User, UserAdmin)
admin.site.register(PasswordResetToken)