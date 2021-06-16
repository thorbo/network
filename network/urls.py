
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("posts", views.posts, name="posts"),
    path("posts/<str:mode>", views.posts),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("profile/<str:profile>", views.profile, name="profile"),
]
