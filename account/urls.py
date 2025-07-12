from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "account"

urlpatterns = [
    #Register view
    path("register/", views.register_view, name="register" ),

    #Login view
    path("login/", views.login_view, name="login"),

    #Delete later
    path("test/", views.test_view, name="test"), #test path DELETE LATER

    #URL RESET PASSWORD
    path("reset-password/", views.reset_password, name="reset_password"),
    path("reset-password-confirm/<str:token>/", views.reset_password_confirm, name="reset_password_confirm"),
    
    #LOGOUT URL.
     # O si necesitas otras URLs de auth, inclúyelas manualmente:
    path("logout/", LogoutView.as_view(), name="logout"),
]
