from rest_framework import serializers
from Mibuddy.models import User, Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'gender'
                  , 'age', 'nationality', 'language', 'occupation'
                  , 'areas', 'herefor', 'aboutme')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('id', 'created', 'userId', 'token')