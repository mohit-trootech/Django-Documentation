# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TablespaceExample, Pizza, Topping, Restaurant, PdfFileModel

admin.site.register(TablespaceExample)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Restaurant)


@admin.register(PdfFileModel)
class PdfFileModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    readonly_fields = ["id"]
    fieldsets = [("PDF Details", {"fields": ["id", "title", "pdf"]})]
