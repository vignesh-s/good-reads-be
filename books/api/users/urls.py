from django.urls import path

from .users_views import current_user, register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("user/", current_user, name="current-user"),
]
