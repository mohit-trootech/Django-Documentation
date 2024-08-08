from email import header
from pickletools import read_uint1
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseNotModified,
    HttpResponseRedirect,
)
from django.shortcuts import render
import datetime
from django.contrib import messages


def request_object(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    messages.info(request, "Hello")
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


def not_found(request):
    return HttpResponseNotFound("Hello")


def redirect_view(request):
    print(request.status_code)
    # return HttpResponseRedirect(redirect_to="/learn/http")
    return HttpResponseNotAllowed(permitted_methods=["POST"])
