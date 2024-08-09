# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from mysite.settings import MEDIA_ROOT, MEDIA_URL
from debug_toolbar.toolbar import debug_toolbar_urls
from schema_graph.views import Schema
from . import views

# from polls.views import InputForm

urlpatterns = [
    path("http/", views.request_object, name="request-object"),
    # path("not_found/", views.not_found, name="not-found"),
    path("redirect_view/", views.redirect_view, name="redirect-view"),
    path("file_form/", views.file_form, name="file-form"),
    path("redirect_view/", views.redirect_view, name="redirect-view"),
    path("pizaa_details", views.PizzaDetails.as_view(), name="pizza-details"),
    path(
        "pizaa_redirect_counter/<int:pk>",
        views.PizzaDetails.as_view(),
        name="pizza-details",
    ),
]
