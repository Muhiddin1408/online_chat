from django.utils.deprecation import MiddlewareMixin
from chat.models import UserBlock
from django.http import JsonResponse


class UserBlockChecknMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                user_block = UserBlock.objects.get(user=request.user)
                if user_block.is_active():
                    return JsonResponse(data={
                        "message": "User has been blocked !",
                        "blocked_until": user_block.blocked_until,
                        "reason": user_block.reason
                        })
                else:
                    pass
            except UserBlock.DoesNotExist:
                pass
