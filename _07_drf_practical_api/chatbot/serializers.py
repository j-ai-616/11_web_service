from rest_framework import serializers
from .models import ChatMessage, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'message_type', 'content', 'created_at']
        read_only_fields = ['id', 'session', 'message_type', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(source='messages.count', read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at', 'updated_at', 'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'message_count']


class ChatSendMessageSerializer(serializers.Serializer):
    # 모델과 직접 연결되지 않은 요청 body 검증에는 일반 Serializer를 사용한다.
    content = serializers.CharField(max_length=3000)
