from django.shortcuts import render
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework import status
from .models import Discount
import json
from datetime import datetime
from .serializer import DiscountSerializer
from rest_framework.views import APIView

# Create your views here.
class DiscountView(APIView):
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        action = request.GET.get('action')
        if not action: 
            return Response({'status': 0, 'error': 'action parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'validate':
            print(request.data)   
            code = request.data.get('code')
            if not code:
                return Response({'status': 0, 'error': 'code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
            discount = Discount.objects.filter(code=code).first()
            if not discount:
                return Response({'status': 0, 'error': 'Invalid discount code'}, status=status.HTTP_400_BAD_REQUEST)
            # confirm the discount is still valid
            if discount.usageCount >= discount.usageLimit:
                return Response({'status': 0, 'error': 'Discount code has reached its usage limit'}, status=status.HTTP_400_BAD_REQUEST)
            # check if the discount has expired
            if discount.expiration < now():
                return Response({'status': 0, 'error': 'Discount code has expired'}, status=status.HTTP_400_BAD_REQUEST)
            # check if the discount is applicable to the current user
            if request.user.id in discount.used_by:
                return Response({'status': 0, 'error': 'Discount code has already been used by you'}, status=status.HTTP_400_BAD_REQUEST)
            # check if the discount is applicable to products in the cart
            if len(discount.applicableProducts) > 0:
                cart_items = request.user.cart_items.all()
                applicable_products = [item for item in cart_items if item.product.id in discount.applicableProducts]
                if len(applicable_products) == 0:
                    return Response({'status': 0, 'error': 'Discount code is not applicable to products in the cart'}, status=status.HTTP_400_BAD_REQUEST)
            # check if the discount is applicable to categories in the cart
            if len(discount.applicableCategories) > 0:
                cart_items = request.user.cart_items.all()
                applicable_categories = [item for item in cart_items if item.product.category.id in discount.applicableCategories]
                if len(applicable_categories) == 0:
                    return Response({'status': 0, 'error': 'Discount code is not applicable to categories in the cart'}, status=status.HTTP_400_BAD_REQUEST)
            # REGISTER THE DISCOUNT USAGE
            # discount.usageCount += 1
            # discount.used_by.append(request.user.id)
            # discount.save()
            return Response({'status': 1, 'discount_data': DiscountSerializer(discount).data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        discount = Discount.objects.get(pk=pk)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)