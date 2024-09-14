from django.http import JsonResponse
from chat.models import UserBlock


def check_is_user_blocked(user):
    try:
        user_block = UserBlock.objects.get(user=user)
        if user_block.is_active():
            return True
        else:
            return False
    except UserBlock.DoesNotExist:
        return False