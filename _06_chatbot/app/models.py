from django.db import models
from django.utils import timezone

# 하나의 상담 세션을 저장하는 모델
class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        # ChatSession.objects.all() 조회 시 최근 수정 된 세션부터 정렬한다.
        ordering = ['-updated_at']

    def __str__(self):
        return self.session_id
    
# 하나의 대화 메세지를 저장하는 모델
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(
        max_length=10, 
        # 저장할 수 있는 값을 제한하는 속성 (실제 DB에는 'human' 또는 'ai'만 저장 된다.)
        choices=[('human', 'Human'), ('ai', 'AI')]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f'{self.session_id} - {self.message_type}: {self.content[:50]}'
    