from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Mibuddy.models import User, Token, ChatGroup, Member, Message, PinnedMessage
from Mibuddy.serializers import UserSerializer, TokenSerializer, ChatGroupSerializer, MemberSerializer, MessageSerializer, PinnedMessageSerializer
from Mibuddy.utils import generate_random_string, is_valid_email


############################################# admin ##############################################

class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class MessageListAdmin(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

#################################### Log in and Sign up Views #####################################

def generate_token():
    while True:
        tokenstr = generate_random_string(40)
        try:
            Token.objects.get(token=tokenstr)
        except:
            break
    return tokenstr


class LogIn(APIView):
    def post(self, request, format=None):
        """
        user can login via this view
        :param request: must contain email and password of user
        :param format:
        :return: {'userId':'35', 'token':'4kd83jsg37sdil2'} if success,
                404 error if there isn't such user, and sometimes 500 error for uncaught exception
        """
        # get email and password from request data
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        # check validation of email
        if is_valid_email(email) is not True:
            return Response({'email': ['Email is not vaild.']}, status=status.HTTP_400_BAD_REQUEST)
        # find user from the email and password
        try:
            user = User.objects.get(email=email, password=password)
        except:
            raise Http404
        # generate token for the user and register it
        tokenstr = generate_token()
        try:
            token = Token.objects.get(userId=user.pk)
            tokenSerializer = TokenSerializer(token, data={'userId': user.pk, 'token': tokenstr})
        except:
            tokenSerializer = TokenSerializer(data={'userId': user.pk, 'token': tokenstr})
        if tokenSerializer.is_valid():
            tokenSerializer.save()
            return Response(tokenSerializer.data)
        return Response(tokenSerializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUp(APIView):
    def post(self, request, format=None):
        """
        user can signup via this view
        :param request: must contain email, password, username, gender(Male/Female), birthday, nationality, language, occupation, areas, herefor, aboutme
        :param format:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


########################################## After login, calls to api use this function to get user #########

def get_user(request):
    """
    Check token and return user
    :param request: must contain token to authenticate
    :param format:
    :return: User model or None
    """
    try:
        token = Token.objects.get(token=request.data['token'])
        user = User.objects.get(pk=token.userId)
        return user
    except:
        return None


########################################## Get user's profile #####################################

class Profile(APIView):
    def post(self, request, format=None):
        """
        Show user's profile
        :param request: only token is needed
        :param format:
        :return:
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data)


########################################## Create a chat room #####################################

class CreateNewGroup(APIView):
    def post(self, request, format=None):
        """
        Create new chat group
        :param request: token, name, community
        :param format:
        :return:
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            # check availabilty of group name
            group = ChatGroup.objects.filter(name=request.data['name'], community=request.data['community'])
            if len(group) != 0:
                return Response({'name': ['group with this name already exists.']}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ChatGroupSerializer(data={'name': request.data['name'], 'leaderId': user.pk, 'community': request.data['community']})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


########################################## Get group list in a certain community with keyword ###########

class GroupList(APIView):
    def post(self, request, format=None):
        """
        returns group list
        :param request: token, community, keyword(optional)
        :param format:
        :return:
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            community = request.data['community']
            if 'keyword' in request.data:
                keyword = request.data['keyword']
            else:
                keyword = ''
            groups = ChatGroup.objects.filter(community=community, name__contains=keyword)
            serializer = ChatGroupSerializer(groups, many=True)
            grouplist = []
            for group in serializer.data:
                leader = User.objects.get(pk=group['leaderId'])
                if leader is None:
                    continue
                grouplist.append({'id': group['id'], 'name': group['name'], 'leader': leader.username, 'community': group['community'], 'created': group['created']})
            return Response(grouplist)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


######################################### Join a group ##################################################

class JoinGroup(APIView):
    def post(self, request, format=None):
        """
        join a group, this is needed to calculate count of members in a group
        :param request: token, groupId
        :param format:
        :return: {'isleader': True} if success.
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        # get groupId
        try:
            groupId = request.data['groupId']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        # check group with groupId
        try:
            group = ChatGroup.objects.get(pk=groupId)
        except:
            raise Http404
        # register member to the group
        try:
            member = Member.objects.get(groupId=groupId, userId=user.pk)
            serializer = MemberSerializer(member)
        except:
            serializer = MemberSerializer(data={'groupId': groupId, 'userId': user.pk})
        if serializer.is_valid():
            return Response({'isleader': group.leaderId == user.pk})
        else:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


######################################### Send a message ####################################################

class SendMessage(APIView):
    def post(self, request, format=None):
        """
        send message to a group
        :param request: token, groupId, message
        :param format:
        :return:
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        # get groupId and message
        try:
            groupId = request.data['groupId']
            message = request.data['message']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        # register message
        serializer = MessageSerializer(data={'userId': user.pk, 'groupId': groupId, 'message': message})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


########################################## Get recent messages in a group #####################################

class MessageList(APIView):
    def post(self, request, format=None):
        """
        get recent messages in a group
        :param request: token, groupId
        :param format:
        :return: {'chatting': [{'username': 'user1', 'isyou': True, 'messages': ['hi', 'how are you?']}, ...], 'pinned': ['Notice', ...]}
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        # get groupId
        try:
            groupId = request.data['groupId']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        # get all messages
        messages = Message.objects.filter(groupId=groupId)
        serializer = MessageSerializer(messages, many=True)
        chatlist = [] # should be result after loop
        templist = [] # ['hi', 'how are you']
        tempid = -1 # id of templist's author
        for chat in serializer.data:
            if chat['userId'] == tempid:
                templist.append({'id': chat['id'], 'message': chat['message']})
            else:
                try:
                    tempuser = User.objects.get(pk=tempid)
                    chatlist.append({'username': tempuser.username, 'messages': templist, 'isyou': (tempuser.pk == user.pk)})
                except:
                    notused = 0
                templist = [{'id': chat['id'], 'message': chat['message']}]
                tempid = chat['userId']
        # last message
        try:
            tempuser = User.objects.get(pk=tempid)
            chatlist.append({'username': tempuser.username, 'messages': templist, 'isyou': (tempuser.pk == user.pk)})
        except:
            notused = 0
        pinnedMessages = PinnedMessage.objects.filter(groupId=groupId)
        serializer = PinnedMessageSerializer(pinnedMessages, many=True)
        pinnedlist = []
        for pinned in serializer.data:
            try:
                message = Message.objects.get(pk=pinned['messageId'])
            except:
                continue
            pinnedlist.append(message.message)
        return Response({'chatting': chatlist, 'pinned': pinnedlist})


####################################### Pin an message ################################################

class PinMessage(APIView):
    def post(self, request, format=None):
        """
        pin a message so that users can see it always
        :param request: token, messageId
        :param format:
        :return:
        """
        user = get_user(request)
        if user is None:
            return Response({'Authentication': 'Please log in first.'}, status=status.HTTP_401_UNAUTHORIZED)
        # check message
        try:
            messageId = request.data['messageId']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message = Message.objects.get(pk=messageId)
        except:
            raise Http404
        # check if user is leader of the group
        try:
            group = ChatGroup.objects.get(pk=message.groupId)
        except:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if group.leaderId != user.pk:
            return Response({'user': 'only leader of group can pin a message'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PinnedMessageSerializer(data={'messageId': messageId, 'groupId': message.groupId})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
