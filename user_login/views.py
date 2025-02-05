from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from _core.utils.helpers import check_if_username_is_phone_or_email

# Create your views here.
def user_login(request):
    message = ''
    errors = []
    if request.method == 'GET' and request.GET.get('message'):
        message = request.GET.get('message')
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

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
    return user.username