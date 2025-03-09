from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Address
from .serializer import AddressSerializer
from _core.utils.helpers import is_email_exists, is_phone_exists, is_business_name_exists
import requests

# Create your views here.
@login_required(login_url='user_login')
def user_profile(request):
    return render(request, 'user_profile.html')

@api_view(['PUT'])
def update_profile(request):
    # get the (parsed) data from the request Object
    data = request.data
    # get the new items to be updated
    user_table_fields = data.get('table_fields')
    # get the user id
    user_id = data.get('user_id')
    # get the user object
    user = User.objects.get(id=user_id)

    # check if user is vendor or user
    if user.profile.user_type == 'vendor':
        return Response({'errors': 'You are not allowed to update this profile.'}, status=status.HTTP_403_FORBIDDEN)
    
    # check if the email exists
    if is_email_exists(user_table_fields.get('email'), user_id):
        return Response({'errors': ['Email already exists for another user.']}, status=status.HTTP_400_BAD_REQUEST)
    if is_phone_exists(user_table_fields.get('phone'), user_id):
        return Response({'errors': 'Phone number already exists for another user.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # extract the profile data
    profile_data = user_table_fields.pop('profile', None)

    # update the user object
    for attr, value in user_table_fields.items():
        setattr(user, attr, value)
    user.save()

    # update the profile object
    if profile_data:
        for attr, value in profile_data.items():
            setattr(user.profile, attr, value)
        user.profile.save()
    
    messages.success(request, 'Profile updated successfully.')

    return Response({'message':'User profile update successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_vendor_profile(request):
    print('update_vendor_profile')
    # get the (parsed) data from the request Object
    data = request.data
    # get the new items to be updated
    user_table_fields = data.get('table_fields')
    # get the user id
    user_id = data.get('user_id')
    # get the user object
    user = User.objects.get(id=user_id)

    # check if user is vendor or user
    if user.profile.user_type == 'user':
        return Response({'errors': 'You are not allowed to update this profile.'}, status=status.HTTP_403_FORBIDDEN)
    
    # check if the email exists
    if is_email_exists(user_table_fields.get('email'), user_id):
        return Response({'errors': 'Email already exists for another user.'}, status=status.HTTP_400_BAD_REQUEST)
    if is_phone_exists(user_table_fields.get('phone'), user_id):
        return Response({'errors': 'Phone number already exists for another user.'}, status=status.HTTP_400_BAD_REQUEST)
    if is_business_name_exists(user_table_fields.get('business_name'), user_id):
        return Response({'errors': 'Business name already exists for another vendor.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # extract the profile data
    profile_data = user_table_fields.pop('profile', None)

    # update the user object
    for attr, value in user_table_fields.items():
        setattr(user, attr, value)
    user.save()

    # update the profile object
    if profile_data:
        for attr, value in profile_data.items():
            setattr(user.profile, attr, value)
        user.profile.save()
    
    messages.success(request, 'Profile updated successfully.')

    return Response({'message':'Vendor profile update successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def change_user_password(request):
    # get the (parsed) data from the request Object
    data = request.data
    # get the new items to be updated
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # get the user id
    user_id = data.get('user_id')

    # get the user object
    user = User.objects.get(id=user_id)

    # validate user
    if not user:
        return Response({'errors': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    # validate the current password
    if not user.check_password(current_password):
        return Response({'errors': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    # update the user password
    user.set_password(new_password)
    user.save()
    message = 'Password changed successfully. Please login again with your new password.'
    messages.success(request, message)

    return Response({'message': message}, status=status.HTTP_200_OK)

# endpoint for managing user addresses
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@login_required(login_url='user_login')
def user_addresses(request):
    user = request.user
    if request.method == 'GET':
        addresses = Address.objects.filter(user=user, deleted=False)
        addresses_serializer = AddressSerializer(addresses, many=True)
        print(addresses_serializer.data)
        return Response({'addresses': addresses_serializer.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        address = Address.objects.create(
            user=user,
            house_address=data.get('house_address'),
            city=data.get('city').lower(),
            city_id=data.get('city_id', None),
            lga=data.get('lga'),
            lga_id=data.get('lga_id', None),
            state=data.get('state'),
            state_id=data.get('state_id', None),
            
            country=data.get('country'),
            country_id=data.get('country_id', None),
            zip=data.get('zip', None),
            phone=data.get('phone', None),
        )
        messages.success(request, 'Address added successfully.')
        address_serializer = AddressSerializer(address)
        return Response({'status':1,'address': address_serializer.data}, status=status.HTTP_201_CREATED)
    if request.method == 'PUT':
        data = request.data
        address_id = data.get('address_id')
        address = Address.objects.get(id=address_id)
        address.house_address = data.get('house_address')
        address.city = data.get('city')
        address.city_id = data.get('city_id')
        address.state = data.get('state')
        address.state_id = data.get('state_id')
        address.country = data.get('country')
        address.country_id = data.get('country_id')
        address.zip = data.get('zip')
        address.phone = data.get('phone')
        address.save()
        address_serializer = AddressSerializer(address)
        return Response({'address': address_serializer.data}, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        data = request.data
        address_id = data.get('address_id')
        address = Address.objects.get(id=address_id)
        address.deleted = True
        address.save()
        return Response({'message': 'Address deleted successfully.'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

# create a proxy for fetching data from external api
@api_view(['GET'])
def fetch_states_data(request):
    url = 'https://gps-naija.onrender.com/states'
    response = requests.get(url)
    data = response.json()
    return Response(data, status=status.HTTP_200_OK)