# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = get_response(request)
        if not request.user.is_authenticated:
            if "polls" in request.path:
                messages.info(request, "Please Login to View This Page")
                return redirect("/learn/http")
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
