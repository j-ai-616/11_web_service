from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT 로그인 API
    # username/password를 받아 access token과 refresh token을 발급하는 DRF 제공 View이다.
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT 재발급 API
    # refresh token을 받아 새로운 access token을 발급하는 DRF SimpleJWT 제공 View이다.
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/auth/', include('accounts.urls')),
    path('api/', include('qna.urls')),
    path('api/chat/', include('chatbot.urls')),

    # OpenAPI schema 생성 API
    # 프로젝트의 API 구조를 Swagger가 읽을 수 있는 문서 데이터(JSON/YAML)로 생성하는 View이다.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI 화면
    # /api/schema/에서 생성한 API 문서 데이터를 브라우저에서 보기 좋게 보여주는 View이다.
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
