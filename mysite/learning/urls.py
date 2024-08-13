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
    path("pizaa_add", views.CreatePizzaView.as_view(), name="pizza-add"),
    path("pizza_list", views.PizzaList.as_view(), name="pizza-list"),
    path("pizaa_details", views.PizzaDetails.as_view(), name="pizza-details"),
    path("pdf_detail/<int:pk>www", views.PdfDetail.as_view(), name="pdf-detail"),
    path("pdf_list", views.PdfList.as_view(), name="pdf-lists"),
    path("pizaa_delete/<int:pk>", views.PizzaDelete.as_view(), name="pizza-delete"),
    path(
        "pizaa_redirect_counter/<int:pk>",
        views.PizzaDetails.as_view(),
        name="pizza-details",
    ),
]
