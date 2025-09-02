from django.contrib import admin
from .models import Link, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "created_at"]
    list_filter = ["created_at", "tags"]
    search_fields = ["title", "url", "summary"]
    filter_horizontal = ["tags"]
    ordering = ["-created_at"]
