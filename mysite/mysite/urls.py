# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from mysite.settings import MEDIA_ROOT, MEDIA_URL
from debug_toolbar.toolbar import debug_toolbar_urls
from schema_graph.views import Schema

# from polls.views import InputForm

urlpatterns = [
    path("", RedirectView.as_view(url="/polls"), name="home"),
    # path("", InputForm.as_view(), name="form"),
    path("polls/", include("polls.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("schema/", Schema.as_view()),
] + debug_toolbar_urls()

urlpatterns = urlpatterns + static(MEDIA_URL, document_root=MEDIA_ROOT)
