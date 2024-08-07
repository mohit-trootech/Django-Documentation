# -*- coding: utf-8 -*-
from django.forms import (
    Form,
    ModelForm,
    TextInput,
    CharField,
    PasswordInput,
    NumberInput,
    EmailInput,
    ClearableFileInput,
)
from accounts.models import User
from django.core.validators import *
from accounts.constants import (
    SIGNUP_FIRST_NAME_LABEL,
    SIGNUP_LAST_NAME_LABEL,
    SIGNUP_USERNAME_LABEL,
    SIGNUP_EMAIL_LABEL,
    SIGNUP_PASSWORD_LABEL,
    SIGNUP_FIRST_NAME_HELP_TEXT,
    SIGNUP_LAST_NAME_HELP_TEXT,
    SIGNUP_USERNAME_HELP_TEXT,
    SIGNUP_EMAIL_HELP_TEXT,
    SIGNUP_PASSWORD_HELP_TEXT,
    LOGIN_USERNAME_LABEL,
    LOGIN_PASSWORD_LABEL,
    LOGIN_USERNAME_HELP_TEXT,
    LOGIN_PASSWORD_HELP_TEXT,
)


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        widgets = {}
        for field in fields:
            if field == "email":
                input_option = EmailInput
            elif field == "password":
                input_option = PasswordInput
            else:
                input_option = TextInput
            widgets[field] = input_option(attrs={"class": "form-control"})
        labels = {
            "first_name": SIGNUP_FIRST_NAME_LABEL,
            "last_name": SIGNUP_LAST_NAME_LABEL,
            "username": SIGNUP_USERNAME_LABEL,
            "email": SIGNUP_EMAIL_LABEL,
            "password": SIGNUP_PASSWORD_LABEL,
        }
        help_texts = {
            "first_name": SIGNUP_FIRST_NAME_HELP_TEXT,
            "last_name": SIGNUP_LAST_NAME_HELP_TEXT,
            "username": SIGNUP_USERNAME_HELP_TEXT,
            "email": SIGNUP_EMAIL_HELP_TEXT,
            "password": SIGNUP_PASSWORD_HELP_TEXT,
        }


class UserLoginForm(Form):
    username = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Login Username"}
        ),
        label=LOGIN_USERNAME_LABEL,
        help_text=LOGIN_USERNAME_HELP_TEXT,
    )
    password = CharField(
        required=True,
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Login Password"}
        ),
        label=LOGIN_PASSWORD_LABEL,
        help_text=LOGIN_PASSWORD_HELP_TEXT,
    )


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "profile",
            "first_name",
            "last_name",
            "email",
            "age",
            "phone",
            "address",
        ]
        widgets = {}
        for field in fields:
            if field == "profile":
                input_option = ClearableFileInput
            elif field == "age" or field == "phone":
                input_option = NumberInput
            elif field == "email":
                input_option = EmailInput
            else:
                input_option = TextInput
            widgets[field] = input_option(attrs={"class": "form-control"})
