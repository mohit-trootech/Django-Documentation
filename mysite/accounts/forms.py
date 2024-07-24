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
            "first_name": "Enter First Name",
            "last_name": "Enter Last Name",
            "username": "Enter Username",
            "email": "Enter Email",
            "password": "Enter Password",
        }
        help_texts = {
            "first_name": "Please Enter First Name",
            "last_name": "Please Enter Last Name",
            "username": "Please Enter Username",
            "email": "Please Enter Email",
            "password": "Please Choose Password",
        }


class UserLoginForm(Form):
    username = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Login Username"}
        ),
        label="Enter Username",
        help_text="Username Required",
    )
    password = CharField(
        required=True,
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Login Password"}
        ),
        label="Enter Password",
        help_text="Password Required",
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
