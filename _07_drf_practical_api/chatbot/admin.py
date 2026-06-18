from django.contrib import admin
from .models import ChatMessage, ChatSession


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['message_type', 'content', 'created_at']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'updated_at']
    search_fields = ['user__username', 'title']
    inlines = [ChatMessageInline]
