from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    # CreateAPIView는 POST 생성 API를 빠르게 만들기 위한 DRF Generic View이다.
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    # JWT 토큰이 유효할 때만 현재 사용자 정보를 반환한다.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
