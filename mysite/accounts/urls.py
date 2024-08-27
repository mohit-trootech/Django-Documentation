# -*- coding: utf-8 -*-
from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("password_change", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change_done",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset_done",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete",
        PasswordResetCompleteView.as_view(
            template_name="accounts/passsword_reset_done.html"
        ),
        name="password_reset_complete",
    ),
]
