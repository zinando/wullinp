from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'