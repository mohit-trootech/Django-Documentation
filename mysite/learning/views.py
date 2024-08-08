# -*- coding: utf-8 -*-
from email import header
from pickletools import read_uint1
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseNotModified,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .forms import UploadFileForm
from .models import Pizza


def request_object(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    response = HttpResponse("Hello This is response")
    response.headers.setdefault("name", "Mohit")
    new_response = HttpResponse(
        headers={
            "Content-Type": "application/vnd.ms-excel",
            "Content-Disposition": 'attachment; filename="foo.xls"',
        },
    )
    not_found = HttpResponseNotFound()
    return render(
        request,
        "temp.html",
        {
            "html": html,
            "response": response,
            "new_response": new_response,
            "not_found": not_found,
        },
    )


# def not_found(request):
#     return HttpResponseNotFound("Hello")


def redirect_view(request):
    print(request.status_code)
    # return HttpResponseRedirect(redirect_to="/learn/http")
    return HttpResponseNotAllowed(permitted_methods=["POST"])


def handle_uploaded_file(f):

    with open("new", "wb") as destination:
        print(destination)
        for chunk in f.chunks():
            destination.write(chunk)


def file_form(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/learn/file_form/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


def redirect_view(request):
    params = Pizza.objects.all()
    return redirect("/learn/file_form", kwargs={params})
