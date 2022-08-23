from django.urls import path
from . import views

app_name="slotbook"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("cp/",views.cp, name="cp")
]
