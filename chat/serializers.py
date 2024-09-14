from rest_framework import serializers

from chat.models import ReportTheme, User, Chat, Massage, UserBlock, UserReport, Years, Apartment


class SerializerUser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'ip', 'login_time', 'choose_years')


class SerializerYears(serializers.ModelSerializer):

    class Meta:
        model = Years
        fields = '__all__'


class SerializerChat(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'


class SerializerMassage(serializers.ModelSerializer):

    class Meta:
        model = Massage
        fields = '__all__'


class ApartmentMassage(serializers.ModelSerializer):

    class Meta:
        model = Apartment
        fields = '__all__'


class SpamThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTheme
        fields = '__all__'


class UserSpamSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    reporter_id = serializers.IntegerField()
    theme_id = serializers.IntegerField()
    chat_id = serializers.IntegerField()
    reason = serializers.CharField()

    class Meta:
        model = UserReport
        fields = ("user_id", "reporter_id", "theme_id", "chat_id", "reason",)
    
    def create(self, validated_data):
        user_id = validated_data.get("user_id")
        reporter_id = validated_data.get("reporter_id")
        theme_id = validated_data.get("theme_id")
        chat_id = validated_data.get("chat_id")
        reason = validated_data.get("reason")

        user = User.objects.filter(id=user_id).first()
        reporter = User.objects.filter(id=reporter_id).first()
        report_theme = ReportTheme.objects.filter(id=theme_id).first()
        chat = Chat.objects.filter(id=chat_id).first()

        if not user or not reporter:
            raise serializers.ValidationError({
                'user_id': 'Invalid user ID.',
                'reporter_id': 'Invalid reporter ID.'
            })

        report = UserReport.objects.create(
            user=user, reporter=reporter,
            theme=report_theme, chat=chat,
            reason=reason)

        return report


class UserInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTheme
        fields = '__all__'


class UserBlockResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserBlock
        fields = ("is_active", "blocked_until", "reason")


class UserReponseSerializer(serializers.ModelSerializer):
    block = UserBlockResponseSerializer()
    class Meta:
        model = User
        fields = ("id", "username", "gender", "years", "ip", "language", "block")