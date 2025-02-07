from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@login_required(login_url='user_login')
def user_profile(request):
    return render(request, 'user_profile.html')

