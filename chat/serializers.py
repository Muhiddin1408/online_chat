from rest_framework import serializers

from chat.models import User, Chat, Massage, Years, Apartment


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
