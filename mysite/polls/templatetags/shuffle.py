# -*- coding: utf-8 -*-
import random
from django import template

register = template.Library()


@register.filter
def shuffle(arg):
    """
    Shuffle the elements of a list or iterable.

    :param arg: The list or iterable to shuffle.
    :return: A new list with elements shuffled.
    """
    try:
        # Convert to list to ensure it can be shuffled
        tmp = list(arg)
        random.shuffle(tmp)
        return tmp
    except TypeError:
        # Handle case where arg is not iterable
        return arg


# @register.filter
# def test(arg):
#     print(arg)
#     return arg
