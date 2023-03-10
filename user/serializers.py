from django.contrib.auth.models import Group
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
                  'url',
                  'username',
                  'first_name',
                  'last_name',
                  'fonction',
                  'email',
                  'groups',
                  'avatar'
                ]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
