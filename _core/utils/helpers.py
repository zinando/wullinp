"""functions that are useful for the rest of the codebase"""
from django.contrib.auth.models import User
from user_register.models import Profile

def check_if_username_is_phone_or_email(username):
    if '@' in username:
        return 'email'
    else:
        return 'phone'


def is_email_exists(email, user_id=None):
    if user_id:
        return User.objects.filter(email=email).exclude(id=user_id).exists()
    return User.objects.filter(email=email).exists()

def is_phone_exists(phone, user_id=None):
    if user_id:
        return Profile.objects.filter(phone=phone).exclude(user_id=user_id).exists()
    return Profile.objects.filter(phone=phone).exists()

def is_business_name_exists(business_name, user_id=None):
    if user_id:
        return Profile.objects.filter(business_name=business_name).exclude(id=user_id).exists()
    return Profile.objects.filter(business_name=business_name).exists()
