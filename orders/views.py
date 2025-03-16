from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from user_profile.models import Address
from user_profile.serializer import AddressSerializer
from products.models import Products
from .serializer import CartItemSerializer
from wishlist.models import Donators
from _core.utils.helpers import calculate_shipping_cost, prepare_order, log_paystack_response
from _core.utils.raw_data import pickup_locations

# Create your views here.
@login_required(login_url='user_login') 
@api_view(['GET','POST', 'PUT'])
def checkoutView(request):
    cart_items = []
    shipping = 0
    discount = {}
    if request.method == 'GET' and request.GET.get('action') == 'confirm-payment':
        txn_ref = request.GET.get('txn_ref', None)
        if txn_ref is None:
            return render(request, 'payment_confirmation.html', {'status': False, 'message': 'No transaction reference provided', 'error': ['Payment not confirmed']})
        # log the order
        response = log_paystack_response(txn_ref)
        if response['status'] > 0:
            return render(request, 'payment_confirmation.html', response['response'])
        
        return render(request, 'payment_confirmation.html', {'status': False, 'message': response['message'], 'error': ['Payment not confirmed']})
    
    elif request.method == 'GET' and request.GET.get('action') == 'confirm-donation':
        txn_ref = request.GET.get('txn_ref', None)
        if txn_ref is None:
            return render(request, 'payment_confirmation.html', {'status': False, 'message': 'No transaction reference provided', 'error': ['Payment not confirmed']})
        # log the order
        response = log_paystack_response(txn_ref, 'donation')
        # get the owner of the item
        donator = Donators.objects.filter(txn_ref=txn_ref).first()
        owner = donator.wishlist.user.first_name + ' ' + donator.wishlist.user.last_name
        if response['status'] > 0:
            if response['status'] == 1:
                response['response']['message'] += f"\n\nYou have successfully donated to {owner}'s wishlist item."
                
            return render(request, 'payment_confirmation.html', response['response'])
        
        return render(request, 'payment_confirmation.html', {'status': False, 'message': response['message'], 'error': ['Payment not confirmed']})
    
    elif request.method == 'GET':
        #get the cart items
        cart_items = CartItem.objects.filter(user=request.user)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        cart_items = cart_items_serializer.data
        user_addresses = Address.objects.filter(user=request.user).all()
        user_addresses_serializer = AddressSerializer(user_addresses, many=True)
        user_addresses = user_addresses_serializer.data
        user_addresses = json.dumps(user_addresses)

    if request.method == 'POST' and request.GET.get('action') == 'save-cart':
        # get the post data
        data = request.data  #list
        cart_items = sync_cart(request, data)

        return Response({'status':1, 'message':'Cart items added successfuly', 'error':[]}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST' and request.GET.get('action') == 'verify-order':
        order_details = request.data
        response = prepare_order(request, order_details)

        return Response(response, status=status.HTTP_200_OK)
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'shipping': shipping, 'discount': discount, 'user_addresses': user_addresses, 'pickup_stations': pickup_locations})

# endpoints for modifying cart items
@api_view(['POST'])
def modifyCartItem(request):
    if request.method == 'POST':
        data = request.data
        action = data.get('action', None)
        item_id = data.get('itemId', None)
        item = data.get('item', None) # dict
        if action is None:
            return Response({'status':0, 'message':'Invalid request', 'error':['Invalid request']}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'delete' and item_id is not None:
            CartItem.objects.filter(id=item_id).delete()
            return Response({'status':1, 'message':'Item deleted successfuly', 'error':[]}, status=status.HTTP_200_OK)
        if action == 'update' and item is not None and isinstance(item, dict):
            cart_item = CartItem.objects.filter(id=item_id).first()
            if cart_item is None:
                return Response({'status':0, 'message':'Item not found', 'error':['Item not found']}, status=status.HTTP_404_NOT_FOUND)
            cart_item.quantity = item.get('quantity', cart_item.quantity)
            cart_item.size = item.get('size', cart_item.size)
            cart_item.color = item.get('color', cart_item.color)
            cart_item.gender = item.get('gender', cart_item.gender)
            cart_item.save()
            return Response({'status':1, 'message':'Item updated successfuly', 'error':[]}, status=status.HTTP_200_OK)
    return Response({'status':0, 'message':'Invalid request', 'error':['Invalid request']}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for calculating shipping cos
@api_view(["POST"])
def get_shipping_cost(request):
    cart_items = request.user.cart_items
    user_address_id = request.data.get('selectedAddressId', 0)
    delivery_method = request.data.get('deliveryMethod', 'pickup')
    delivery_type = request.data.get('deliveryType', 'regular')
    if Address.objects.filter(id=user_address_id).exists():
        user_address = Address.objects.filter(id=user_address_id).first()
        shipping_cost = calculate_shipping_cost(cart_items, user_address, delivery_method, delivery_type)
        return Response({"status":1, "shipping_cost": shipping_cost}, status=status.HTTP_200_OK)
    return Response({"status":0}, status=status.HTTP_404_ADDRESS_NOT_FOUND)

def sync_cart(request, cartItems):
    cart_items = []
    # delete all cart items
    CartItem.objects.filter(user=request.user).delete()
    
    for item in cartItems:
        
        product = Products.objects.filter(id=item['productId']).first()
        if product is None:
            continue

        cart_item = CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=item['quantity'],
            size=item.get('size', None),
            color=item.get('color', None),
            gender=item.get('gender', None)
        )
        cart_item_serializer = CartItemSerializer(cart_item)
        cart_items.append(cart_item_serializer.data)
    return cart_items
    
