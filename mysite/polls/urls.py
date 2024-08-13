# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from . import views
from polls.models import Question

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
    path("users", views.PollsUsers.as_view(), name="polls-users"),
    path(
        "archive_index/",
        ArchiveIndexView.as_view(
            model=Question,
            date_field="created",
            paginate_by=100,
            context_object_name="latest",
        ),
        name="archive-index",
    ),
    path(
        "archive_index/<int:year>",
        views.QuestionYearArchiveView.as_view(),
        name="archive-index-year",
    ),
    path(
        "archive_index/<int:year>/<str:month>",
        views.QuestionMonthArchiveView.as_view(),
        name="archive-index-month",
    ),
]
