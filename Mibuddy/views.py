from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Mibuddy.models import User, Token
from Mibuddy.serializers import UserSerializer, TokenSerializer
from Mibuddy.utils import generate_random_string, is_valid_email


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
            return Response({'detail': 'Email is not vaild.'}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
