"""
URL configuration for _01_django_project project.

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
# from first import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('first/', views.index)
    # 루트 URL로 접속하면 first 앱으로 리다이렉트
    path('', RedirectView.as_view(url='first/', permanent=True)),
    # first.urls 모듈의 url_patterns를 연결
    path('first/', include('first.urls')),
    path('second/', include('second.urls'))
]
