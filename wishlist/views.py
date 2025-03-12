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
    # wishlist = MySavedProduct.objects.filter(user=user).all()
    # wishlist_serializer = MySavedProductSerializer(wishlist, many=True)
    user_serializer = UserSerializer(user)
    wishlist = user_serializer.data['wishlist']
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'owner': f'{user.first_name} {user.last_name}', 'request_url': request.build_absolute_uri()})

# create CBV for wishlist
class WishlistView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'status': 0, 'message': 'You must be logged in to add to wishlist'}, status=status.HTTP_403_FORBIDDEN)
        
        #get the product details
        product_id = request.data['productId']
        # if the product is already in the wishlist, modify its attributes
        if MySavedProduct.objects.filter(product=product_id, user=request.user).exists():
            product = MySavedProduct.objects.get(product=product_id, user=request.user)
            product.quantity = request.data['quantity']
            product.size = request.data['size']
            product.color = request.data['color']
            product.gender = request.data.get('gender', None)
            product.save()
        else:
            product = MySavedProduct.objects.create(
                product=Products.objects.get(id=product_id),
                user=request.user,
                quantity=request.data['quantity'],
                size=request.data['size'],
                color=request.data['color'],
                gender=request.data.get('geder', None)
            )
        count = request.user.wishlist.count()
        return Response({'status': 1, 'message': f'{request.data.get("productName")} added to wishlist', 'count':count}, status=status.HTTP_201_CREATED)


    def put(self, request):
        """This method is used to donate to a wishlist"""
        userData = request.data
        if not userData['name'] or not userData['email'] or not userData['phone'] or not userData['amount'] or not userData['wishId']:
            return Response({'status': 0, 'message': 'Missing fields detected in the user data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass