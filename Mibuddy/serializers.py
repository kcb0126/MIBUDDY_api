from rest_framework import serializers
from Mibuddy.models import User, Token, ChatGroup, Member, Message, PinnedMessage


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


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ('id', 'created', 'name', 'leaderId', 'community')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields =('joined', 'groupId', 'userId')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'created', 'userId', 'groupId', 'message')


class PinnedMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinnedMessage
        fields = ('messageId', 'groupId')