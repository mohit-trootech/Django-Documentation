# -*- coding: utf-8 -*-
import random
from django import template

register = template.Library()


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


@register.filter
def test(arg):
    print(arg)
    return arg
