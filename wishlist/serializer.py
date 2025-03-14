from rest_framework import serializers
from .models import MySavedProduct, Donators
from products.serializer import ProductSerializer
import math
from orders.models import Order, PGRequest


class DonatorsSerializer(serializers.ModelSerializer):
    payment_successful = serializers.SerializerMethodField()
    class Meta:
        model = Donators
        fields = '__all__'

    def get_payment_successful(self, obj):
        status = False
        txn = PGRequest.objects.filter(ref_id=obj.txn_ref).first()
        if txn and txn.res_status == 'SUCCESS':
            status = True
        return status


class MySavedProductSerializer(serializers.ModelSerializer):
    donators = DonatorsSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)
    contribution_percentage = serializers.SerializerMethodField()
    contributed_amount = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()
    is_fully_paid = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    donator_count = serializers.SerializerMethodField()
    class Meta:
        model = MySavedProduct
        fields = '__all__'

    def get_sub_total(self, obj):
        return float(obj.product.cprice) * obj.quantity

    def get_total_cost(self, obj):
        return self.get_sub_total(obj) + obj.shipping_cost

    def get_contributed_amount(self, obj):
        # get the first donor
        # if obj.donators.count() > 0:
        #     order = Order.objects.get(order_type='WISHLIST')
        #     if order.user == obj.user:
        #         obj.order = order
        #         obj.save()
        if obj.order:
            transactions = obj.order.transactions.all()
            if len(transactions) > 0:
                return sum(
                    transaction.amount
                    for transaction in transactions
                    if transaction.res_status == 'SUCCESS'
                )
        return 0

    def get_contribution_percentage(self, obj):
        contributed_amount = self.get_contributed_amount(obj)
        total_cost = self.get_total_cost(obj)
        if contributed_amount > 0:
            return math.ceil((contributed_amount / total_cost) * 100)
        return 0

    def get_is_fully_paid(self, obj):
        contributed_amount = self.get_contributed_amount(obj)
        total_cost = self.get_total_cost(obj)
        return contributed_amount >= total_cost

    def get_remaining_amount(self, obj):
        contributed_amount = self.get_contributed_amount(obj)
        total_cost = self.get_total_cost(obj)
        return total_cost - contributed_amount

    def get_user_id(self, obj):
        return obj.user.id
    
    def get_donator_count(self, obj):
        counter = 0
        donators = obj.donators.all()
        if donators:
            for donator in donators:
                txn = PGRequest.objects.filter(ref_id=donator.txn_ref).first()
                if txn and txn.res_status == 'SUCCESS':
                    counter += 1
        return counter