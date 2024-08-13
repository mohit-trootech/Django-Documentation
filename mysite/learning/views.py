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
import pprint
from django.views.generic import (
    RedirectView,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
)
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.contrib import messages
from .forms import UploadFileForm
from .models import Pizza, PdfFileModel


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


class PizzaRedirectView(RedirectView):
    pattern_name = "pizza-details"
    query_string = True

    def get_redirect_url(self, *args, **kwargs) -> str | None:
        pizza = get_object_or_404(Pizza, pk=kwargs["pk"])
        return super().get_redirect_url(*args, **kwargs)


class PizzaDetails(DetailView):
    model = Pizza
    template_name = "pizza_details.html"

    def get_queryset(self):
        return super().get_queryset()

    def get_slug_field(self) -> str:
        return super().get_slug_field()


class CreatePizzaView(CreateView):
    model = Pizza
    fields = "__all__"
    template_name = "createPizza.html"
    success_url = "/learn/pizza_list"


class PizzaList(ListView):
    model = Pizza
    template_name = "pizzaList.html"
    context_object_name = "pizzas"


class PizzaDelete(DeleteView):
    model = Pizza
    template_name = "pizzaDelete.html"
    success_url = "/learn/pizza_list"


class PdfDetail(DetailView):
    model = PdfFileModel
    template_name = "pdf_detail.html"
    context_object_name = "pdf"


class PdfList(ListView):
    model = PdfFileModel
    template_name = "pdf_list.html"
    context_object_name = "pdfs"
