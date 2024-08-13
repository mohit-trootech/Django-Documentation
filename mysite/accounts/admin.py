# -*- coding: utf-8 -*-
from accounts.models import User
from django.contrib import admin
from accounts.constants import (
    STATUS_INACTIVE_BOOL,
    STATUS_ACTIVE_BOOL,
    USER_ADMIN_STATUS_UNACTIVE_DESCRIPTION,
    USER_ADMIN_STATUS_ACTIVE_DESCRIPTION,
)

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

admin.site.register(ContentType)
admin.site.register(Permission)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "is_active"]
    readonly_fields = ["id"]
    fieldsets = [
        (
            "Customer Details",
            {
                "fields": [
                    "id",
                    "profile",
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password",
                    "age",
                    "address",
                    "phone",
                ]
            },
        ),
        (
            "Status Details",
            {
                "classes": ["collapse"],
                "fields": ["is_staff", "is_superuser", "is_active"],
            },
        ),
        (
            "Login Details",
            {"classes": ["collapse"], "fields": ["date_joined", "last_login"]},
        ),
        (
            "Group Details",
            {"classes": ["collapse"], "fields": ["groups", "user_permissions"]},
        ),
    ]
    search_fields = ["username"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    ordering = ["id"]
    actions = ["mark_inactive", "mark_active"]

    @admin.action(description=USER_ADMIN_STATUS_UNACTIVE_DESCRIPTION)
    def mark_inactive(self, request, queryset):
        for instantce in queryset:
            instantce.is_active = STATUS_INACTIVE_BOOL
            instantce.save(update_fields=["is_active"])

    @admin.action(description=USER_ADMIN_STATUS_ACTIVE_DESCRIPTION)
    def mark_active(self, request, queryset):
        for instantce in queryset:
            instantce.is_active = STATUS_ACTIVE_BOOL
            instantce.save(update_fields=["is_active"])
