# -*- coding: utf-8 -*-
from django.contrib import admin
from polls.models import Question, Choice, Tag
from polls.constants import (
    VOTE_RESET,
    CHOICE_TOTAL_VOTES_RESET_DESCRIPTION,
    QUESTION_TOTAL_VOTES_RESET_DESCRIPTION,
)
from django.contrib import messages
from django.utils.translation import ngettext


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
                    "tag",
                    "image",
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
        # for instance in queryset:
        #     instance.total_votes = VOTE_RESET
        #     instance.save(update_fields=["total_votes"])
        updated = queryset.update(total_votes=VOTE_RESET)
        self.message_user(
            request,
            ngettext(
                "%d votes was successfully been reset.",
                "%d votes were successfully been reset.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


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
        # for instantce in queryset:
        #     instantce.votes = VOTE_RESET
        #     instantce.save(update_fields=["votes"])
        updated = queryset.update(votes=VOTE_RESET)
        self.message_user(
            request,
            ngettext(
                "%d vote was successfully been reset.",
                "%d votes were successfully been reset.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
