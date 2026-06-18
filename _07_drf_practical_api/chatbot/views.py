from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatSession
from .permissions import IsChatSessionOwner
from .serializers import ChatMessageSerializer, ChatSendMessageSerializer, ChatSessionSerializer
from .services import send_message
from .throttles import ChatbotRateThrottle


class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated, IsChatSessionOwner]

    def get_queryset(self):
        # 사용자별 데이터 격리를 위해 현재 사용자의 세션만 조회한다.
        return ChatSession.objects.filter(user=self.request.user).prefetch_related('messages')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        # ViewSet의 custom action으로 특정 세션의 메시지 목록 API를 제공한다.
        session = self.get_object()
        serializer = ChatMessageSerializer(session.messages.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], throttle_classes=[ChatbotRateThrottle])
    def send(self, request, pk=None):
        # 챗봇 메시지 전송 API에만 별도 throttle을 적용한다.
        session = self.get_object()
        serializer = ChatSendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _, ai_message = send_message(session, serializer.validated_data['content'])
        return Response(ChatMessageSerializer(ai_message).data, status=status.HTTP_201_CREATED)
