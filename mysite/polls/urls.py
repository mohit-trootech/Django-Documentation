# -*- coding: utf-8 -*-
from django.urls import path

from . import views

# urlpatterns = [
#     path("", views.index, name="index"),
#     path("<int:question_id>", views.detail, name="details"),
#     path("<int:question_id>/results", views.results, name="results"),
#     path("<int:question_id>/vote", views.vote, name="vote"),
# ]

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("vote", views.vote, name="vote"),
    path("add", views.PollsCreate.as_view(), name="polls-create"),
]
