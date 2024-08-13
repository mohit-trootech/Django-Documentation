# -*- coding: utf-8 -*-
from django.forms import *
from polls.models import Question, Tag
from polls.constants import (
    POLL_TAG_LABEL,
    POLL_TITLE_LABEL,
    POLL_IMAGE_LABEL,
    POLL_TITLE_HELP_TEXT,
    POLL_IMAGE_HELP_TEXT,
    POLL_TAG_HELP_TEXT,
    POLLS_TITLE_PLACEHOLDER,
    POLLS_IMAGE_PLACEHOLDER,
    POLLS_TAG_PLACEHOLDER,
)
from accounts.models import User
from django.contrib.auth.models import Group

# class NameForm(Form):
#     username = CharField(
#         required=True,
#         max_length=30,
#         widget=TextInput(
#             attrs={"class": "form-control mb-3", "placeholder": "Enter Login Username"}
#         ),
#         label="Enter Username",
#         help_text="Username is required field",
#     )
#     password = CharField(
#         required=True,
#         max_length=30,
#         widget=PasswordInput(
#             attrs={
#                 "class": "form-control mb-3",
#                 "placeholder": "Choose Password",
#                 "type": "password",
#                 "title": "Please Enter Password in Required Format",
#             }
#         ),
#         label="Enter Password",
#         help_text="Password Should Less than 8 Character with a Combination of one small, one capital, one number & one special Character",
#     )


class CreatePoll(ModelForm):

    use_required_attribute = False

    class Meta:
        model = Question
        fields = ["title", "image", "tag"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": POLLS_TITLE_PLACEHOLDER,
                    "required": "true",
                }
            ),
            "image": ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "placeholder": POLLS_IMAGE_PLACEHOLDER,
                    "accept": "image/*",
                }
            ),
            "tag": Select(
                attrs={
                    "class": "form-select text-capitalize",
                    "placeholder": POLLS_TAG_PLACEHOLDER,
                },
            ),
        }
        labels = {
            "title": POLL_TITLE_LABEL,
            "image": POLL_IMAGE_LABEL,
            "tag": POLL_TAG_LABEL,
        }

        help_texts = {
            "title": POLL_TITLE_HELP_TEXT,
            "image": POLL_IMAGE_HELP_TEXT,
            "tag": POLL_TAG_HELP_TEXT,
        }

    def __init__(self, *args, **kwargs):
        super(CreatePoll, self).__init__(*args, **kwargs)
        self.fields["tag"].queryset = Tag.objects.all()


class UserGroupEdit(ModelForm):
    class Meta:
        model = User
        fields = ["id", "groups"]
        widgets = {
            "username": TextInput(attrs={"hidden": "true"}),
            "groups": SelectMultiple(attrs={"class": "form-control"}),
        }
