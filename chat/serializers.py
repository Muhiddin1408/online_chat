from rest_framework import serializers

from chat.models import User, Chat, Massage, Years


class SerializerUser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


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
