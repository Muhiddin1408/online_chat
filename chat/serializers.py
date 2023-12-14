from rest_framework import serializers

from chat.models import User


class SerializerUser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
