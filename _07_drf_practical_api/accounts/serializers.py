from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    # write_only는 요청에는 포함되지만 응답 JSON에는 노출되지 않게 한다.
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        read_only_fields = ['id']

    def create(self, validated_data):
        # API 입력값을 검증한 뒤 serializer가 직접 객체 생성 로직을 담당할 수 있다.
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']
