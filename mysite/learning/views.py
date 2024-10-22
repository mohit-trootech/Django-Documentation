# -*- coding: utf-8 -*-
from email import header
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseNotModified,
    HttpResponseRedirect,
)
from django.views.generic import (
    RedirectView,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    TemplateView,
    FormView,
)
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.contrib import messages
from .forms import UploadFileForm, SendEmail
from .models import Pizza, PdfFileModel
from django.contrib.messages.views import SuccessMessageMixin


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
    not_allowed = HttpResponseNotAllowed
    response.set_cookie("key", "value")
    print(request.COOKIES)
    print(response.cookies)
    return render(
        request,
        "temp.html",
        {
            "html": html,
            "response": response,
            "new_response": new_response,
            "not_found": not_found,
            "not_allowed": not_allowed,
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


class CreatePizzaView(CreateView, SuccessMessageMixin):
    model = Pizza
    fields = "__all__"
    template_name = "createPizza.html"
    success_url = "/learn/pizza_list"
    success_message = "permission Not Allowed"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perms(["learning.add_pizza"]):
            messages.info(request, "Permission Not Allowed")
            return HttpResponseRedirect("/polls")
        return super().dispatch(request, *args, **kwargs)


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


class EmailSendView(FormView):
    template_name = "email_send.html"
    form_class = SendEmail
    success_url = "/learn/send_email"

    def form_valid(self, form):
        from django.contrib.messages import info
        from django.core.mail import send_mass_mail, EmailMultiAlternatives
        from django.template.loader import render_to_string

        subject = form.cleaned_data.get("subject")
        sender = form.cleaned_data.get("sender")
        receiver = form.cleaned_data.get("receiver").split(",")
        attachment = form.cleaned_data.get("attachment")
        body = "Temp Body"
        print(receiver)
        try:
            mail = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=sender,
                to=receiver,
            )
            html_message = render_to_string(
                "email.html",
                context={"user": self.request.user, "from": sender},
            )
            mail.attach_alternative(html_message, "text/html")
            if attachment:
                mail.attach("image.jpeg", attachment.read())
            mail.send()
            info(self.request, "Mail Send Successfully")
        except Exception as e:
            form.add_error(None, e)
            return super().form_invalid(form)
        return super().form_valid(form)
