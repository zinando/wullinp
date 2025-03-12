from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from _core.utils.helpers import check_if_username_is_phone_or_email
from orders.views import sync_cart
import json

# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out from your previous account.', extra_tags='alert alert-info')
    message = ''
    errors = []
    if request.method == 'GET' and request.GET.get('message'):
        message = request.GET.get('message')
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        cart = request.POST.get('cart', None)

        # check if username is email or phone
        username_type = check_if_username_is_phone_or_email(user_id)
        if username_type == 'email':
            username = fetch_username_with_email(user_id)
        else:
            username = user_id[-10:] # get last 10 characters of phone number
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            message = 'Login Successful'

            # update user cart
            if cart:
                sync_cart(request, json.loads(cart))
        else:
            errors.append('Invalid Username or Password')
        
        if len(errors) == 0:
            # display success message
            messages.success(request, message)

            # check for next parameter in URL
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('home')
        
    return render(request, 'user_login.html', {'error_messages': errors, 'success_message': message})
    
def fetch_username_with_email(email):
    user = User.objects.filter(email=email).first()
    if user:
        return user.username
    return None