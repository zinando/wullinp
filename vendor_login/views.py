from django.shortcuts import render, redirect
from vendor_register.models import Vendor
from user_register.models import Profile
from _core.utils.helpers import check_if_username_is_phone_or_email
from django.contrib import messages
# import login, authenticate
from django.contrib.auth import authenticate, login, logout
#from .auth_backends import VendorBackend

# Create your views here.
def vendor_login(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out from your previous account.', extra_tags='alert alert-info')
        
    if request.method == 'POST':
        user_id = request.POST['username']
        password = request.POST['password']
        username_type = check_if_username_is_phone_or_email(user_id)

        if username_type == 'email':
            username = fetch_username_with_email(user_id)
        else:
            username = user_id[-10:]
        try:
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                print(f'User: {user}')
                print(f'is user authenticated: {user.is_authenticated}')
                print(f'is user recognized: {request.user}')
                print(f'is vendor instance: {isinstance(request.user, Vendor)}')
                messages.success(request, 'Login Successful')
                # check for next parameter in URL
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                return redirect('vendor_dashboard')
            else:
                messages.error(request, 'Invalid Username or Password')
        except Exception as e:
            messages.error(request, f'{e}')
    print(f'Vendor username: {request.user}')
    return render(request, 'vendor_login.html')


def fetch_username_with_email(email):
    user = Vendor.objects.filter(email=email).first()
    if user:
        return user.username
    return None