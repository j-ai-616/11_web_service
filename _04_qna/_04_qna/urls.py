"""
URL configuration for _04_qna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qna/', include('qna.urls')),
    # 루트 경로로 접속하면 '/qna/' 경로로 이동시킨다.
    # permanent=False: 임시 리다이렉트(HTTP 302)
    # permanent=True: 영구 리다이렉트(HTTP 301) -> 브라우저 캐싱
    path('', RedirectView.as_view(url='/qna/', permanent=False)),
    path('uauth/', include('uauth.urls'))
]

# 개발 환경에서만 media 파일을 Django 개발 서버가 제공하도록 설정
if settings.DEBUG:
    # /media/로 시작하는 URL 요청이 오면 MEDIA_ROOT 폴더에서 해당 파일을 찾아 응답하게 설정
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
