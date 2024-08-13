# -*- coding: utf-8 -*-
import json
import random
from polls.models import Tag, Question
from faker import Faker

tags_list = [
    "anime",
    "bollywood",
    "art",
    "books",
    "comics",
    "dating",
    "relationship",
    "pride",
    "indian",
    "festival",
    "gaming",
    "finance",
    "money",
    "holiday",
    "news",
    "nature",
    "religion",
    "sports",
    "shopping",
    "travel",
    "technology",
    "school",
    "college",
    "miscellaneous",
]


def generate_random_poll(index):
    question = f"Sample Poll Question {index}"
    return {"title": question, "tag": Tag.objects.get(title=random.choice(tags_list))}


polls = [generate_random_poll(i) for i in range(1001, 100000)]


def generate_random_choice(index):
    choices = f"Option {index}B"
    return {
        "title": choices,
        "question": Question.objects.get(title=f"Sample Poll Question {index}"),
    }


# Generate 1000 records
choices = [generate_random_choice(i) for i in range(1001, 100000)]
