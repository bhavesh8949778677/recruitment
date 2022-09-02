from django.urls import path
from . import views

app_name="slotbook"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("cp/",views.cp, name="cp"),
    path("sports_pages/<str:sport>",views.sports_pages,name="sports_pages"),
    path("profile/",views.profile, name="profile"),
    path("newpage/",views.newpage, name="newpage"),
    path("newslot/",views.newslot, name="newslot"),
    path("sports_pages/<str:sport>/edit",views.edit, name="edit"),
    path("newstaff/", views.newstaff, name="newstaff"),
    path("cancel/", views.cancel, name="cancel"),
    path("deletestaff/", views.deletestaff, name="deletestaff"),
    path("unava/", views.unava, name="unava"),
    path("have/", views.have, name="have"),
    path("book/", views.book, name="book"),
]
