"""Mibuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from Mibuddy import views

urlpatterns = [
    url(r'^admin/users/$', views.UserList.as_view()),
    url(r'^admin/messages/$', views.MessageListAdmin.as_view()),

    url(r'^login/$', views.LogIn.as_view()),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^profile/$', views.Profile.as_view()),

    url(r'^create/$', views.CreateNewGroup.as_view()),
    url(r'groups/$', views.GroupList.as_view()),
    url(r'join/$', views.JoinGroup.as_view()),

    url(r'send/$', views.SendMessage.as_view()),
    url(r'messages/$', views.MessageList.as_view()),
    url(r'pin/$', views.PinMessage.as_view()),
]
