from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
# Create your views here.

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
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            pass
        else:
            return render(request, "registration/login.html", {"error" : {"Invalid credentials."}})
        
        return render(request, "login.html")
        