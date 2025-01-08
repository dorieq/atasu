from rest_framework import serializers
from .models import (UserModel)
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'groups', 'pfp', 'first_name', 'last_name']


class UserPFPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['pfp']