from rest_framework import serializers
from .models import Answer, Question


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class AnswerSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    vote_count = serializers.IntegerField(source='voters.count', read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'question', 'author', 'content', 'created_at', 'modified_at', 'vote_count', 'is_author']
        read_only_fields = ['id', 'question', 'author', 'created_at', 'modified_at', 'vote_count', 'is_author']

    def get_is_author(self, obj):
        # SerializerMethodField는 요청 사용자 기준의 계산 필드를 응답에 포함할 때 사용한다.
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and obj.author_id == request.user.id)


class QuestionListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    answer_count = serializers.IntegerField(source='answers.count', read_only=True)
    vote_count = serializers.IntegerField(source='voters.count', read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'author', 'subject', 'created_at', 'modified_at', 'answer_count', 'vote_count', 'is_author']
        read_only_fields = fields

    def get_is_author(self, obj):
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and obj.author_id == request.user.id)


class QuestionDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    vote_count = serializers.IntegerField(source='voters.count', read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'author', 'subject', 'content', 'created_at', 'modified_at', 'vote_count', 'is_author', 'answers']
        read_only_fields = ['id', 'author', 'created_at', 'modified_at', 'vote_count', 'is_author', 'answers']

    def get_is_author(self, obj):
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and obj.author_id == request.user.id)


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'subject', 'content']
        read_only_fields = ['id']
