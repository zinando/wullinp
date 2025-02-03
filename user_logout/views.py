from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')