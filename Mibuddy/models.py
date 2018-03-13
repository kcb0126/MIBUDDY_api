from django.db import models
from pycountry import countries

GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
COUNTRY_CHOICES = list((item.name, item.name) for item in countries)


class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='male', max_length=100)
    age = models.IntegerField()
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
