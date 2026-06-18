from rest_framework.permissions import BasePermission


class IsChatSessionOwner(BasePermission):
    # 사용자별 채팅 세션은 본인만 조회/삭제/메시지 전송할 수 있어야 한다.
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.user_id == request.user.id)
