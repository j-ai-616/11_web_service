from django.db import models
from django import forms
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions')
    subject = models.CharField(max_length=200) 
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True) 

# django model form 클래스 : 사용자 입력을 위한 모델 클래스
# - 입력 값 처리, 검증 기능 수행
# - 입력 값을 모델 객체로 변환
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        # 사용자 입력을 위한 필드
        fields = ['subject', 'content']
        # 사용자 화면에 노출 될 필드명
        labels = {
            'subject' : '제목',
            'content' : '내용'
        }
