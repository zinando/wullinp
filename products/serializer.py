# import serilizer
from rest_framework import serializers
from .models import Products, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    """This class defines the serializer for the ProductCategory model"""
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """This class defines the serializer for the Products model"""
    category = ProductCategorySerializer(read_only=True)
    class Meta:
        model = Products
        fields = '__all__'


    