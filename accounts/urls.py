from django.urls import path
from .views import register_user, login_user, logout_user, current_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("me/", current_user, name="current_user"),
]
