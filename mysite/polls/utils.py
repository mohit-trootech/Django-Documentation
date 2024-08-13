# -*- coding: utf-8 -*-
from polls.models import Choice, Question
from typing import Dict, Any, Pattern
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


def serialize_data_set_for_ajax_update(id: int) -> Dict[str, Any]:
    """
    Create Updated dataset Based on Question Queryset

    :param id: The ID of the Question to serialize.
    :return: A dictionary containing the updated data.
    """
    choice_data = {}
    question = Question.objects.get(id=id)
    for choice in question.choice.all():
        choice_data[choice.id] = {"title": choice.title, "votes": choice.votes}

    updated_data = {
        "question_total_votes": question.total_votes,
        "choices_data": choice_data,
    }
    return updated_data


def find_pattern(patt: Pattern, text: str) -> bool:
    """
    Check if a pattern matches any part of the text.

    :param patt: The regular expression pattern to search for.
    :param text: The text to search within.
    :return: True if the pattern is found, False otherwise.
    """
    return bool(re.search(patt, text))


def validate(password: str) -> bool:
    """
    Validate the given password based on specific criteria.

    :param password: String of password received from form.
    :return: Boolean indicating if the password is valid.
    """
    if 6 < len(password) < 13:
        return (
            find_pattern(r"[A-Z]", password)
            and find_pattern(r"[a-z]", password)
            and find_pattern(r"\d", password)
            and find_pattern(r"[$#@!%^&*]", password)
        )
    return False
