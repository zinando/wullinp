from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MySavedProduct, Donators
from products.models import Products
from django.contrib.auth.models import User
from .serializer import MySavedProductSerializer
from _core.serializer import UserSerializer
from orders.models import Order, CartItem, OrderItem, PGRequest
from user_profile.serializer import AddressSerializer
from _core.utils.helpers import calculate_shipping_cost, delete_first_donor_order
import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
#@login_required(login_url='user_login')
def wishlist(request):
    # get id parameter from the url
    id = request.GET.get('id')
    if not id or id == 'None':
        return redirect('user_login')
    # get the serialized wishlist
    user = User.objects.get(id=id)
    if not user:
        return redirect('4_oh_4')
    user_serializer = UserSerializer(user)
    wishlist = user_serializer.data['wishlist']
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'owner': f'{user.first_name} {user.last_name}', 'request_url': request.build_absolute_uri()})

# route for displaying wishlist donators
def wishlist_donators(request):
    # get id parameter from the url
    wishId = request.GET.get('id')
    if not wishId or wishId == 'None':
        return redirect('user_login')
    # get the serialized wishlist
    wishlist = MySavedProduct.objects.get(id=wishId)
    if not wishlist:
        return redirect('4_oh_4')
    wishlist_serializer = MySavedProductSerializer(wishlist)
    wishlist = wishlist_serializer.data
    
    return render(request, 'wishlist_donators.html', {'wishlist': wishlist})

# create CBV for wishlist
class WishlistView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        """This method is used to add a product to the wishlist"""
        if not request.user.is_authenticated:
            return Response({'status': 0, 'message': 'You must be logged in to add to wishlist'}, status=status.HTTP_403_FORBIDDEN)
        
        # create cart model instance using the product details
        cart_data = {
            'user': User.objects.get(id=request.user.id),
            'product': Products.objects.get(id=request.data['productId']),
            'quantity': request.data['quantity'],
            'size': request.data.get('size', None),
            'color': request.data.get('color', None),
            'gender': request.data.get('gender', None),
        }
        my_carts = [CartItem(**cart_data)]

        # calculate the shipping cost with the cart data
        selected_user_address = request.user.addresses.filter(id=request.data['addressId']).first()
        user_address = AddressSerializer(selected_user_address).data
        shipping_cost = calculate_shipping_cost(my_carts, user_address, request.data['deliveryMethod'], request.data['deliveryType'])

        # Add delivery options to the user address
        user_address['deliveryMethod'] = request.data['deliveryMethod']
        user_address['deliveryType'] = request.data['deliveryType']
        
        # if the product is already in the wishlist, modify its attributes
        if MySavedProduct.objects.filter(product=request.data['productId'], user=request.user).exists():
            product = MySavedProduct.objects.get(product=request.data['productId'], user=request.user)
            product.quantity = request.data['quantity']
            product.size = request.data.get('size', None)
            product.color = request.data.get('color', None)
            product.shipping_cost = shipping_cost
            product.shipping_info = user_address
            product.gender = request.data.get('gender', None)
            product.save()
        else:
            product = MySavedProduct.objects.create(
                product=Products.objects.get(id=request.data['productId']),
                user=request.user,
                quantity=request.data['quantity'],
                size=request.data.get('size', None),
                color=request.data.get('color', None),
                gender=request.data.get('geder', None),
                shipping_cost=shipping_cost,
                shipping_info=user_address,
            )
        count = request.user.wishlist.count()
        return Response({'status': 1, 'message': f'{request.data.get("productName")} added to wishlist', 'count':count}, status=status.HTTP_201_CREATED)


    def put(self, request):
        """This method is used to donate to a wishlist"""
        first_donor = False
        userData = request.data
        if not userData['name'] or not userData['email'] or not userData['phone'] or not userData['amount'] or not userData['wishId']:
            return Response({'status': 0, 'message': 'Missing fields detected in the user data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get the wish item
        wish = MySavedProduct.objects.get(id=userData['wishId'])
        serialized_wish = MySavedProductSerializer(wish).data

        # check if the product has been paid in full or if the donation amount is more than the remaining balance
        if serialized_wish['remaining_amount'] <= 0 or userData['amount'] > serialized_wish['remaining_amount']:
            return Response({'status': 0, 'message': 'The donation amount is more than the remaining balance'}, status=status.HTTP_400_BAD_REQUEST)

        # check if the user has an order
        order = wish.order
        if not order:
            first_donor = True
            order = Order.objects.create(
                user=wish.user,
                sub_total = serialized_wish['sub_total'],
                total = serialized_wish['total_cost'],
                shipping_cost = wish.shipping_cost,
                delivery_address = wish.shipping_info['house_address'],
                delivery_city = wish.shipping_info['city'],
                delivery_state = wish.shipping_info['state'],
                delivery_country = wish.shipping_info['country'],
                delivery_method = wish.shipping_info['deliveryMethod'],
                delivery_type = wish.shipping_info['deliveryType'],
                #txn_ref = models.CharField(max_length=100, null=True, blank=True)
                order_type = 'WISHLIST',
                payment_method = 'PAYSTACK',
            )

            # Create orderitem
            OrderItem.objects.create(
                order=order,
                product=wish.product,
                quantity=wish.quantity,
                current_price=wish.product.cprice,
                total_price=serialized_wish['sub_total'],
                color=wish.color,
                size=wish.size,
                gender = wish.gender,
                customer_approved = True,
                system_approved = True,
                customer_approved_date = wish.rdate,
                system_approved_date = wish.rdate,
            )

            # update the wishlist order
            wish.order = order
            wish.save()
        
        # Create a payment gateway request instance
        txn = PGRequest.objects.create(
            order=order,
            amount=userData['amount'],
            customer_email=userData['email'],
        )

        # update order txn_ref with the txn referenceid
        # order.txn_ref = txn.ref_id
        # order.save()

        # save the donor data
        Donators.objects.create(
            wishlist = wish,
            fullname= userData['name'],
            mobile= userData['phone'],
            email= userData['email'],
            amount= userData['amount'],
            personal_message= userData.get('message', None),
            txn_ref= txn.ref_id,
        )

        # prepare the donor data
        order_data = {
            'amount': userData['amount'],
            'email': userData['email'],
            'reference': txn.ref_id,
            'name': userData['name'],
            'phone': userData['phone'],
            'paystackPublicKey': os.getenv('PAYSTACK_PUBLIC_KEY'),
            'paymentPurpose': 'Wishlist Donation',
            'userData': userData,
            'first_donor': first_donor,
        }

        return Response({'status': 1, 'message': 'Donation request initiated', 'order': order_data}, status=status.HTTP_200_OK)



    def delete(self, request):
        """This method is used to remove a product from the wishlist"""
        productName = ''
        if request.data.get('action') == 'delete-first-donor-order':
            # get the txn reference
            txn_ref = request.data['txn_ref']
            # delete the first donor order
            delete_first_donor_order(txn_ref)
            return Response({'status': 1, 'message': 'Donation order removed successfully'}, status=status.HTTP_200_OK)
        if not request.user.is_authenticated:
            return Response({'status': 0, 'message': 'You must be logged in to remove from wishlist'}, status=status.HTTP_403_FORBIDDEN)
        
        # get the item id from the request data
        wishId = request.data['wishId']
        # get the product from the wishlist
        wish = MySavedProduct.objects.get(id=wishId)
        productName = wish.product.name
        # check if the item has an order
        if wish.order:
            return Response({'status': 0, 'message': 'You cannot remove an item that has been ordered'}, status=status.HTTP_400_BAD_REQUEST)
        # delete the product from the wishlist
        wish.delete()
        count = request.user.wishlist.count()
        return Response({'status': 1, 'message': f'{productName} removed from wishlist', 'count':count}, status=status.HTTP_200_OK)
    
