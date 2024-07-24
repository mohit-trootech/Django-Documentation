# -*- coding: utf-8 -*-
from polls.models import Choice, Question, Tag
from django.db.models import F
import re


def update_vote_data_choice_id(data: dict):
    """
    Update Model Votes with Choice.id & Question.id

    :param data: dict

    """
    choice = Choice.objects.get(id=data["choiceId"])
    question = Question.objects.get(id=data["questionId"])
    choice.votes = F("votes") + 1
    question.total_votes = F("total_votes") + 1
    choice.save(update_fields=["votes"])
    question.save(update_fields=["total_votes"])
    return serialize_data_set_for_ajax_update(data["questionId"])


def serialize_data_set_for_ajax_update(id):
    """
    Create Updated dataset Based on Question Queryset

    :param id
    """
    choice_data = {}
    question = Question.objects.get(id=id)
    for i in question.choice.all():
        choice_data[i.id] = {"title": i.title, "votes": i.votes}
    updated_data = {
        "question_total_votes": question.total_votes,
        "choices_data": choice_data,
    }
    return updated_data


def find_pattern(patt, text):
    m = re.search(patt, text)
    if m:
        return True
    else:
        return False


def validate(password: str) -> bool:
    """
    Password Validation

    :param password: str
    :return: bool
    """
    if 6 < len(password) < 13:
        if (
            find_pattern(r"[A-Z]", password)
            and find_pattern(r"[a-z]", password)
            and find_pattern(r"\d", password)
            and find_pattern(r"[$#A]", password)
        ):
            return True
        else:
            return False
    else:
        return False
