from django.contrib import admin
from .models import Answer, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'author', 'created_at']
    search_fields = ['subject', 'content', 'author__username']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'author', 'created_at']
    search_fields = ['content', 'author__username']
