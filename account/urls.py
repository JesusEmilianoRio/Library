from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.register_view, name="register" ),
    path("login/", views.login_view, name="login"),
    path("test/", views.test_view, name="test"), #test path DELETE LATER
    path("", include("django.contrib.auth.urls")),
]
