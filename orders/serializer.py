from rest_framework import serializers
from .models import CartItem, Order, OrderItem, PGRequest, UserCards
from products.serializer import ProductSerializer
from _core.serializer import UserSerializer, ProfileSerializer



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'