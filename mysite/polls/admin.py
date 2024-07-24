# -*- coding: utf-8 -*-
from django.contrib import admin
from polls.models import Question, Choice, Tag
from mysite.constants import (
    VOTE_RESET,
    CHOICE_TOTAL_VOTES_RESET_DESCRIPTION,
    QUESTION_TOTAL_VOTES_RESET_DESCRIPTION,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = [
        "id",
        "title",
    ]
    ordering = ["id"]
    readonly_fields = ["id"]
    fieldsets = [
        (
            "Tag Details",
            {
                "classes": ["extrapretty"],
                "fields": [
                    "id",
                    "title",
                ],
            },
        ),
    ]
    search_fields = ["title"]
    filter = ["title"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    date_hierarchy = "created"
    search_fields = ["title"]
    list_display = [
        "title",
        "total_votes",
        "created",
    ]
    readonly_fields = ["id", "created", "modified", "thumbnail_preview"]
    fieldsets = [
        (
            "Question Details",
            {
                "fields": [
                    "id",
                    "title",
                    "description",
                    "total_votes",
                    "question_tag",
                    "question_image",
                ],
            },
        ),
        (
            "Additional Information",
            {"classes": ["collapse"], "fields": ["created", "modified"]},
        ),
        (
            "Thumbnail Preview",
            {"classes": ["collapse"], "fields": ["thumbnail_preview"]},
        ),
    ]
    search_fields = ["title"]
    list_filter = ["created", "modified"]
    ordering = ["-created"]
    actions = ["mark_reset"]

    @admin.action(description=QUESTION_TOTAL_VOTES_RESET_DESCRIPTION)
    def mark_reset(self, request, queryset):
        for instantce in queryset:
            instantce.total_votes = VOTE_RESET
            instantce.save(update_fields=["total_votes"])


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    model = Choice
    list_display = ["title", "votes", "created"]
    ordering = ["title"]
    readonly_fields = ["id", "created", "modified"]
    fieldsets = [
        (
            "Choice Details",
            {
                "classes": ["extrapretty"],
                "fields": ["id", "title", "votes", "created", "modified"],
            },
        ),
        (
            "Reference Question",
            {
                "fields": ["question"],
            },
        ),
    ]
    search_fields = ["title", "question__title"]
    filter = ["title"]
    actions = ["mark_reset"]

    @admin.action(description=CHOICE_TOTAL_VOTES_RESET_DESCRIPTION)
    def mark_reset(self, request, queryset):
        for instantce in queryset:
            instantce.votes = VOTE_RESET
            instantce.save(update_fields=["votes"])
