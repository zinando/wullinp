from rest_framework import serializers
from .models import MySavedProduct, Donators
from products.serializer import ProductSerializer
import math


class DonatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donators
        fields = '__all__'


class MySavedProductSerializer(serializers.ModelSerializer):
    donators = DonatorsSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)
    contribution_percentage = serializers.SerializerMethodField()
    contributed_amount = serializers.SerializerMethodField()
    is_fully_paid = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = MySavedProduct
        fields = '__all__'

    def get_contribution_percentage(self, obj):
        if obj.order:
            transactions = obj.order.transactions.all()
            if len(transactions) > 0:
                total = sum([transaction.amount for transaction in transactions if transaction.res_status == 'SUCCESS'])
                if total > 0:
                    return math.ceil((total) / obj.product.cprice * 100)
        return 0
    
    def get_contributed_amount(self, obj):
        if obj.order:
            transactions = obj.order.transactions.all()
            if len(transactions) > 0:
                return sum([transaction.amount for transaction in transactions if transaction.res_status == 'SUCCESS'])
        return 0
    
    def get_is_fully_paid(self, obj):
        if obj.order:
            transactions = obj.order.transactions.all()
            if len(transactions) > 0:
                total = sum([transaction.amount for transaction in transactions if transaction.res_status == 'SUCCESS'])
                if total >= obj.product.cprice:
                    return True
        return False
    
    def get_remaining_amount(self, obj):
        if obj.order:
            transactions = obj.order.transactions.all()
            if len(transactions) > 0:
                total = sum([transaction.amount for transaction in transactions if transaction.res_status == 'SUCCESS'])
                return obj.product.cprice - total
        return float(obj.product.cprice)
    
    def get_user_id(self, obj):
        return obj.user.id