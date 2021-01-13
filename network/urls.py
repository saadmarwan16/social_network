from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new_post"),
    path("profile/<int:poster_id>", views.profile, name="profile"),
    path("user-profile", views.user_profile, name="user_profile"),
    path("following", views.following, name="following"),

    # API routes
    path("like", views.like, name="like"),
    path("like-count", views.like_count, name="like_count"),
    path("change-password", views.change_password, name="change_password"),
    path("edit-post", views.edit_post, name="edit_post"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
]
