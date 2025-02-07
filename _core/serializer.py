from rest_framework import serializers
from django.contrib.auth.models import User
from user_register.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'first_name', 'last_name', 'is_staff', 'is_active', 
                  'date_joined', 'last_login', 'groups', 'user_permissions']
        
