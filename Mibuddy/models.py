from django.db import models
from pycountry import countries

GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
COUNTRY_CHOICES = list((item.name, item.name) for item in countries)
COMMUNITY_CHOICES = [('Travel', 'Travel'), ('Countries', 'Countries'), ('Night Life', 'Night Life'), ('Dating', 'Dating')
                     , ('Studies', 'Studies'), ('Business', 'Business'), ('Dining', 'Dining'), ('Housing', 'Housing')]


class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='Male', max_length=100)
    age = models.IntegerField(default=0)
    nationality = models.CharField(choices=COUNTRY_CHOICES, default='Netherlands', max_length=100)
    language = models.CharField(max_length=100, blank=True, default='')
    occupation = models.CharField(max_length=100, blank=True, default='')
    areas = models.CharField(max_length=100, blank=True, default='')
    herefor = models.CharField(max_length=100, blank=True, default='')
    aboutme = models.TextField(blank=True, default='')


class Token(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    userId = models.IntegerField()
    token = models.CharField(max_length=100)


class ChatGroup(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    leaderId = models.IntegerField()
    community = models.CharField(choices=COMMUNITY_CHOICES, max_length=100)

    class Meta:
        ordering = ('created', )


class Member(models.Model):
    joined = models.DateTimeField(auto_now_add=True)
    groupId = models.IntegerField()
    userId = models.IntegerField()


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    userId = models.IntegerField()
    groupId = models.IntegerField()
    message = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created', )


class PinnedMessage(models.Model):
    messageId = models.IntegerField()
    groupId = models.IntegerField()