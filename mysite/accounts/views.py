# -*- coding: utf-8 -*-
from django.views.generic import FormView, View, UpdateView
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserLoginForm, UserCreationForm, UserUpdateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import User
from accounts.constants import (
    LOGIN_ERROR,
    LOGIN_TEMPLATE,
    HOME_URL,
    SIGNUP_TEMPLATE,
    LOGIN_URL,
    PROFILE_TEMPLATE,
)


class LoginView(FormView):
    template_name = LOGIN_TEMPLATE
    form_class = UserLoginForm
    success_url = HOME_URL

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if not user:
            form.add_error(None, LOGIN_ERROR)
            return super().form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class SignupView(FormView):
    template_name = SIGNUP_TEMPLATE
    form_class = UserCreationForm
    success_url = LOGIN_URL

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    template_name = PROFILE_TEMPLATE
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"pk": self.request.user.pk})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(HOME_URL)
