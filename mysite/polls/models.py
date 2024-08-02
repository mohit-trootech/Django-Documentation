# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
import datetime
from django.utils.html import format_html
from polls.constants import (
    THUMBNAIL_PREVIEW_HTML,
    THUMBNAIL_PREVIEW_TAG,
    QUESTION_MEDIA_PATH,
)


class Tag(TitleDescriptionModel):

    def __str__(self):
        return self.title

    class meta:
        ordering = ["title"]


class Question(TitleDescriptionModel, TimeStampedModel):

    total_votes = models.IntegerField(default=0)
    question_image = models.ImageField(
        upload_to=QUESTION_MEDIA_PATH, blank=True, null=True
    )
    question_tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="question",
    )

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now

    @property
    def thumbnail_preview(self):
        if self.question_image:
            return format_html(THUMBNAIL_PREVIEW_TAG.format(self.question_image.url))
        return format_html(THUMBNAIL_PREVIEW_HTML)


class Choice(TitleDescriptionModel, TimeStampedModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choice"
    )
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class meta:
        ordering = ["title"]
