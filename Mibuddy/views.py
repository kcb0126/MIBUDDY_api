from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Mibuddy.models import User, Token
from Mibuddy.serializers import UserSerializer, TokenSerializer
from Mibuddy.utils import generate_random_string, is_valid_email


############################################# admin ##############################################

class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
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
            return Response(status=status.HTTP_400_BAD_REQUEST)
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


########################################## After log in, do several action via these views! #####################

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

