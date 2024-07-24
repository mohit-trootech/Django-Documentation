# -*- coding: utf-8 -*-
from django.db.models import F
from django.utils import timezone
from django.views.generic import *
from polls.models import Question, Choice
from django.http import JsonResponse
from polls.utils import update_vote_data_choice_id, validate
import json
from polls.forms import QuestionForm, NameForm


class InputForm(FormView):
    template_name = "Temp.html"
    form_class = NameForm
    success_url = "/polls"

    def form_valid(self, form):
        username = self.request.POST["username"]
        password = self.request.POST["password"]
        validate_password = validate(password)
        if not validate_password:
            form.add_error(None, "Please Enter Password In Required Format.")
            return super().form_invalid(form)
        print("Valid Successfully", username, password)
        return super().form_valid(form)


class IndexView(ListView):
    template_name = "polls/home.html"
    context_object_name = "questions"
    paginate_by = 10

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(created__lte=timezone.now()).order_by("?")


def vote(request):
    data = json.loads(request.POST["data"])
    updated_data = update_vote_data_choice_id(data)
    return JsonResponse(updated_data)


class PollsCreate(FormView):
    template_name = "polls/polls_create.html"
    form_class = QuestionForm
    success_url = "/polls"

    def form_valid(self, form):
        # Save the question
        question = form.save()

        # Process choices
        choices = self.request.POST.getlist("choices")
        for choice_text in choices:
            if choice_text:  # Check if choice_text is not empty
                Choice.objects.create(question=question, title=choice_text)

        return super().form_valid(form)
