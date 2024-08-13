# -*- coding: utf-8 -*-
import requests
from pprint import pprint

url = "https://medium.com/django-unleashed/advanced-django-models-tips-and-tricks-django-86ef2448aff0"

response = requests.get(url)

print(response.status_code)

pprint(response.content.decode())
