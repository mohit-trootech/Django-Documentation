# -*- coding: utf-8 -*-
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Login Username"}
        ),
    )
    file = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control"}))


class SendEmail(forms.Form):
    subject = forms.CharField(
        max_length=64,
        widget=forms.TextInput(
            attrs={"class": "form-control", "value": "Test Subject"}
        ),
    )
    sender = forms.EmailField(
        max_length=64,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "value": "mohit.prajapat@trootech.com"}
        ),
    )
    receiver = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "value": "mohit.prajapat@trootech.com"}
        ),
        help_text="add mutltiple emails with `,` Seperated",
    )
    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "accepts": "image"}),
    )
