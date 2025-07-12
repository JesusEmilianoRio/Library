from django.shortcuts import render, redirect
from .models import User, PasswordResetToken
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('account:login')

    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form" : form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("account:test") #NEED MODIFICATION

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("account:test") #NEED MODIFICATION
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form" : form})

#View that reset password.    
def reset_password(request):
    if request.method == "POST":
        #Destructure POST variables.
        email_data = request.POST['email']
        
        #If mail does not exists send an error.
        if not email_data:
            messages.error('Insert your email, please.')
            return render(request, 'registration/password_reset.html')

        try:
            #Find user by email
            user = get_object_or_404(User, email = email_data)

            #Clean expired tokens
            PasswordResetToken.cleanup_expired_token()

            #Delete previous unused tokens by the user.
            PasswordResetToken.objects.filter(user = user, used = False).delete()

            #Generate Token
            reset_token = get_random_string(40)
            
            #Save token in DB
            PasswordResetToken.objects.create(
                user = user,
                token = reset_token
            )

            #Build URL of reset.
            reset_url = request.build_absolute_uri(reverse('account:reset_password_confirm', kwargs={'token' : reset_token}))

            #Send Email
            subject = 'Restablecer contraseña'
            message = f"""
            Hola {user.first_name or user.username},
            
            Has solicitado restablecer tu contraseña.
            
            Haz clic en el siguiente enlace para continuar:
            {reset_url}
            
            Este enlace expirará en 1 hora.
            
            Si no solicitaste este cambio, puedes ignorar este email.
            
            Saludos,
            El equipo de soporte.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Se ha enviado un email con instrucciones para restablecer tu contraseña.')
            return redirect('account:login')
        
        #In case user doesn't exist.
        except User.DoesNotExist:
            messages.error(request, 'If email does not exist, you will receive instructions for reset your password.')
            return render(request, 'account:login')

        #In case something went wrong.
        except Exception as e:
            messages.error(request, 'Something went wrong. Try again, please')
            return render(request, 'registration/password_reset.html')


    return render(request, 'registration/password_reset.html')

def reset_password_confirm(request, token):
    reset_user = None
    #Find a valid token
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
        
        if not token_obj.is_valid():
            messages.error(request, 'The linked expired.')
            return redirect('account:login')
        
        # El usuario real está en token_obj.user
        reset_user = token_obj.user

    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid link.')
        return redirect('account:login')

    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #Validate passwords
        if not password1 or not password2:
            messages.error(request, 'Please fulfill all inputs.')
            return render(request, 'registration/password_reset_confirm.html', {
                "token": token,
                "reset_user": reset_user  # Pasar el usuario al template
            })

        if password1 != password2:
            messages.error(request, 'Passwords are not the same.')
            return render(request, 'registration/password_reset_confirm.html', {
                "token": token,
                "reset_user": reset_user  # Pasar el usuario al template
            })

        if len(password1) < 8:
            messages.error(request, 'The password must contain more than 8 characters')
            return render(request, 'registration/password_reset_confirm.html', {
                "token": token,
                "reset_user": reset_user  # Pasar el usuario al template
            })

        #Update password
        user = token_obj.user
        user.password = make_password(password1)
        user.save()

        #Mark token as used
        token_obj.mark_as_used()

        messages.success(request, 'Your password has been changed.')
        return redirect('account:login')

    # GET METHOD
    return render(request, 'registration/password_reset_confirm.html', {
        'token': token,
        'reset_user': reset_user  # Pasar el usuario al template
    })

#TEST VIEW DELETE LATER
@login_required
def test_view(request):
    return render(request, 'registration/test.html', {})