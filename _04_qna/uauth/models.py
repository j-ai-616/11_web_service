from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# User 모델에 추가 정보를 붙이기 위한 모델
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    profile = models.ImageField(upload_to='profile/', null=True, blank=True)

# 회원가입 폼
# Django가 제공하는 UserCreationForm을 상속하여 기본 회원 가입 기능을 사용한다.
class UserForm(UserCreationForm):
    # 기본 UserCreationForm에는 없는 추가 입력 필드는 직접 선언
    birthday = forms.DateField(label='Birthday', required=False)
    profile = forms.ImageField(label='Profile', required=False)

    class Meta:
        model = User
        # 회원가입 화면에서 입력 받을 User 모델의 필드 
        fields = ["username", "password1", "password2", "email"]