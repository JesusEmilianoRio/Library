from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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
    


#TEST VIEW DELETE LATER
@login_required
def test_view(request):
    return render(request, 'registration/test.html', {})