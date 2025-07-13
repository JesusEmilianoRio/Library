from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

#Class that register a User
User = get_user_model()

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20,
                               help_text="Choose a unique username",
                               required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

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

    #Custom hook to validate email
    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email


