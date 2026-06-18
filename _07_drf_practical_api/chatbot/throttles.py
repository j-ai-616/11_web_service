from rest_framework.throttling import UserRateThrottle


class ChatbotRateThrottle(UserRateThrottle):
    # scope를 분리하면 챗봇 API만 별도 요청 제한을 적용할 수 있다.
    scope = 'chatbot'
