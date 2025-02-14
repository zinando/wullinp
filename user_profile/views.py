from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth.models import User
from _core.utils.helpers import is_email_exists, is_phone_exists, is_business_name_exists

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