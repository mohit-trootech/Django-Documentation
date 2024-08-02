# -*- coding: utf-8 -*-
from django.db.models import F
from django.utils import timezone
from django.views.generic import *
from polls.models import Question, Choice
from django.http import HttpResponse, JsonResponse
from polls.utils import update_vote_data_choice_id
import json
from polls.forms import CreatePoll
from polls.constants import (
    HOME_TEMPLATE,
    QUESTION_CONTEXT,
    CREATE_POLLS_TEMPLATE,
    HOME_URL,
)


# class InputForm(FormView):
#     template_name = "Temp.html"
#     form_class = NameForm
#     success_url = "/polls"

#     def form_valid(self, form):
#         username = self.request.POST["username"]
#         password = self.request.POST["password"]
#         validate_password = validate(password)
#         if not validate_password:
#             form.add_error(None, PASSWORD_VALIDATION_ERROR)
#             return super().form_invalid(form)
#         return super().form_valid(form)


class IndexView(ListView):
    template_name = HOME_TEMPLATE
    context_object_name = QUESTION_CONTEXT
    paginate_by = 10

    def get_queryset(self):
        """
        Return the Published Question data Order by Date Newest First
        """
        return Question.objects.filter(created__lte=timezone.now()).order_by("-created")


def vote(request) -> JsonResponse:
    """
    handles the ajax request to update model and send serialize data for javascript in json format

    :param request: question_id
    :return: str
    """
    data = json.loads(request.POST["data"])
    updated_data = update_vote_data_choice_id(data)
    return JsonResponse(updated_data)


class PollsCreate(FormView):
    template_name = CREATE_POLLS_TEMPLATE
    form_class = CreatePoll
    success_url = HOME_URL

    def form_valid(self, form) -> HttpResponse:
        """
        saves the question objects received from form & get choices list and create choices objects for same question

        :param form: unknown
        :return: HttpResponse
        """
        # Save the question
        question = form.save()

        # Process choices
        choices = self.request.POST.getlist("choices")
        for choice_text in choices:
            if choice_text:
                Choice.objects.create(question=question, title=choice_text)
        return super().form_valid(form)
