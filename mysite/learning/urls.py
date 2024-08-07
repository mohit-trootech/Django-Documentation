# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from mysite.settings import MEDIA_ROOT, MEDIA_URL
from debug_toolbar.toolbar import debug_toolbar_urls
from schema_graph.views import Schema
from .views import current_datetime

# from polls.views import InputForm

urlpatterns = [
    path("", current_datetime, name="learning-index"),
]
