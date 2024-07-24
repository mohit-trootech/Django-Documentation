# -*- coding: utf-8 -*-
from django.forms import *
from polls.models import Question, Tag


class NameForm(Form):
    username = CharField(
        required=True,
        max_length=30,
        widget=TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Enter Login Username"}
        ),
        label="Enter Username",
        help_text="Username Required",
    )
    password = CharField(
        required=True,
        max_length=30,
        widget=PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Choose Password",
                "type": "password",
                "title": "Please Enter Password in Required Format",
            }
        ),
        label="Enter Password",
        help_text="Password Should Less than 8 Character with a Combination of one small, one capital, one number & one special Character",
    )


class QuestionForm(ModelForm):

    use_required_attribute = False

    class Meta:
        model = Question
        fields = ["title", "question_image", "question_tag"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Please Enter Question",
                    "required": "true",
                }
            ),
            "question_image": ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Choose Question",
                    "accept": "image/*",
                }
            ),
            "question_tag": Select(
                choices=Tag.objects.all(),
                attrs={"class": "form-select"},
            ),
        }
        labels = {
            "title": "Enter Form Question",
            "question_image": "Enter Question Image",
            "question_tag": "Select Tag",
        }

        help_texts = {
            "title": "Please Enter a Question",
            "question_image": "Choosing Image is Optional",
            "question_tag": "If not choose Tag will be choose automatically",
        }
