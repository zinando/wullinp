"""functions that are useful for the rest of the codebase"""
from django.contrib.auth.models import User
from user_register.models import Profile
from products.models import ProductCategory, Products
import uuid
import re

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

def get_user_object(user_id):
    return User.objects.get(id=user_id)

def get_product_object(product_id):
    return Products.objects.get(id=product_id)

def sanitize_string(my_string):
    """Replaces invalid characters in the public_id with underscores"""
    return re.sub(r'[^a-zA-Z0-9/_-]', '_', my_string)

def check_if_category_has_products(category_id, min_products=1):
    """This function checks if a category has at least min_products"""
    category = ProductCategory.objects.get(id=category_id)
    return category.products.count() >= min_products

# def generate_skux():
#     return str(uuid.uuid4().hex[:10]).upper()
