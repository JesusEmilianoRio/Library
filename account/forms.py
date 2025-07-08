from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

#Class that register a User
User = get_user_model()

def validate_unique_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError("This username is already taken.")
    
def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("This email is already taken.")

class RegistrationForm(UserCreationForm):
    username = forms.CharField(validators=[validate_unique_username])
    email = forms.EmailField(validators=[validate_unique_email])
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]



