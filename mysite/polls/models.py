# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
import datetime
from django.utils.html import format_html


class Tag(TitleDescriptionModel):

    def __str__(self):
        return self.title

    class meta:
        ordering = ["title"]
        verbose_name = "Tags"


class Question(TitleDescriptionModel, TimeStampedModel):

    total_votes = models.IntegerField(default=0)
    question_image = models.ImageField(
        upload_to="Question_Images/", blank=True, null=True
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
            return format_html(
                '<img src="{}" width="320"/>'.format(self.question_image.url)
            )
        return format_html(
            """<div class="warning" style="color:#000;width: 320px;
        padding: 12px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: start;
        background: #FEF7D1;
        border: 1px solid #F7C752;
        border-radius: 5px;
        box-shadow: 0px 0px 5px -3px #111;">
        <div class="warning__icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" viewBox="0 0 24 24" height="24" fill="none">
                <path fill="#393a37" d="m13 14h-2v-5h2zm0 4h-2v-2h2zm-12 3h22l-11-19z" style="
        fill: #F7C752;"></path>
            </svg>
        </div>
        <strong>No Question Image Available</strong>
    </div>"""
        )

    class meta:
        ordering = ["?"]
        verbose_name = "Polls Question"


class Choice(TitleDescriptionModel, TimeStampedModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choice"
    )
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class meta:
        ordering = ["title"]
        verbose_name = "Choices"
