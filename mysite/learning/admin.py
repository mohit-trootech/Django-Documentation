from django.contrib import admin
from .models import TablespaceExample, Pizza, Topping, Restaurant

admin.site.register(TablespaceExample)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Restaurant)
