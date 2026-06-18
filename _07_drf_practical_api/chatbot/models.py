from django.conf import settings
from django.db import models
from django.utils import timezone


class ChatSession(models.Model):
    # 사용자별 채팅 세션을 만들기 위해 User와 1:N 관계를 둔다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=100, default='새 채팅')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-updated_at', '-id']

    def __str__(self):
        return f'{self.user} - {self.title}'


class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('human', 'Human'),
        ('ai', 'AI'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f'{self.session_id} - {self.message_type}: {self.content[:50]}'
