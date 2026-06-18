from django.conf import settings
from django.db import models


class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_votes', blank=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_votes', blank=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return self.content[:50]
