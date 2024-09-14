from celery import shared_task
from chat.models import Chat, RestrictedWord, User, UserBlock, UserReport, ReportTheme
from conf.cache.redis import RedisCache
from django.db import IntegrityError

@shared_task
def check_restricted_word(message: str, user_id: int, chat_id: int):
    restricted_words = RestrictedWord.objects.values_list("title", flat=True)
    message_words = set(message.lower().split())
    for message_word in message_words:
        for restricted_word in restricted_words:
            if restricted_word.lower() in message_word:
                reporter = User.objects.get(is_superuser=True)
                theme = ReportTheme.objects.get(name="abusive_word")
                chat = Chat.objects.get(id=chat_id)
                user = User.objects.get(id=user_id)
                reason = f"Used abusive word like |{message_word}| in chat: {chat_id}"
                UserReport.objects.create(
                    reporter=reporter, user=user, chat=chat,
                    theme=theme, reason=reason)
                user_abusive_words = RedisCache.get(key=f"user_{user.id}")
                print(user_abusive_words)
                if user_abusive_words:
                    RedisCache.set(f"user_{user.id}", value=int(user_abusive_words) + 1)
                else:
                    RedisCache.set(f"user_{user.id}", value=1)
                if user_abusive_words and int(user_abusive_words) >= 10:
                    user_block = UserBlock.objects.get_or_create(
                        id=user.id,
                        defaults={
                            "user": user
                        }
                    )[0]
                    user_block.ban_user(reason=reason, banned_by=reporter)
                    RedisCache.set(f"user_{user.id}", value=1)
                return True
    return False