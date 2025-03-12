from rest_framework import serializers
from .models import MySavedProduct, Donators


class DonatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donators
        fields = '__all__'


class MySavedProductSerializer(serializers.ModelSerializer):
    donators = DonatorsSerializer(many=True, read_only=True)
    class Meta:
        model = MySavedProduct
        fields = '__all__'