# -*- coding: utf-8 -*-
# Status Toggle Boolean

VOTE_RESET = 0

# Descriptions
QUESTION_TOTAL_VOTES_RESET_DESCRIPTION = "Mark Selected Items to Reset Total Votes"
CHOICE_TOTAL_VOTES_RESET_DESCRIPTION = "Mark Selected Items to Reset Votes"


# Question Model Contants
QUESTION_MEDIA_PATH = "Question_Images/"


# Question Model Thumbnail Preview
THUMBNAIL_PREVIEW_TAG = '<img src="{}" width="320"/>'
THUMBNAIL_PREVIEW_HTML = """<div class="warning" style="color:#000;width: 320px;
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


# Errors
PASSWORD_VALIDATION_ERROR = "Password Format Incorrect"

# Templates
HOME_TEMPLATE = "polls/home.html"
CREATE_POLLS_TEMPLATE = "polls/polls_create.html"
POLLS_LIST_TEMPLATE = "polls/polls_list.html"
# URLS
HOME_URL = "/polls"

# Context Object Name
QUESTION_CONTEXT = "questions"

# Form Label Constants
POLL_TITLE_LABEL = "enter poll question"
POLL_IMAGE_LABEL = "enter question image"
POLL_TAG_LABEL = "select poll tag"

# Poll Create Form Help Text

POLL_TITLE_HELP_TEXT = "Please Enter a Question"
POLL_IMAGE_HELP_TEXT = "Choosing Image is Optional"
POLL_TAG_HELP_TEXT = "If not choose Tag will be choose automatically"

# Poll Form Input Placeholders

POLLS_TITLE_PLACEHOLDER = "Please Enter Poll"
POLLS_IMAGE_PLACEHOLDER = "Choose Image File"
POLLS_TAG_PLACEHOLDER = "Please Choose Tag"
