from auth.jwt import decode_jwt
from chat.models import User
from django.http import JsonResponse
from utils import check_is_user_blocked


class UserBlockChecknMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser:
            response = self.get_response(request)
            return response
        if request.path == "/me/" or request.path == "/register/":
            response = self.get_response(request)
            return response
        else:
            # Here we are decoding token data if not admin
            try:
                token = request.environ.get("HTTP_AUTHORIZATION").split()[1]
                payload = decode_jwt(token=token)
                user = User.objects.get(id=payload.get("user_id"))
                if not check_is_user_blocked(user=user):
                    response = self.get_response(request)
                    return response
                return JsonResponse(data={
                        "message": "User has been blocked !",
                        "blocked_until": user.block.blocked_until,
                        "reason": user.block.reason
                        })
            except Exception:
                return JsonResponse(data={
                    "message": "Unauthorized",
                    "status": 401
                })
