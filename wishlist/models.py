from django.db import models as db
from django.contrib.auth.models import User
from products.models import Products
from orders.models import Order

# Create your models here.
class MySavedProduct(db.Model):
    product = db.ForeignKey(Products, on_delete=db.CASCADE, related_name='wishlist')
    user = db.ForeignKey(User, on_delete=db.CASCADE, related_name='wishlist')
    order = db.ForeignKey(Order, on_delete=db.CASCADE, null=True, blank=True, related_name='wishlist')
    quantity = db.IntegerField(default=1)
    size = db.CharField(max_length=10, null=True, blank=True)
    color = db.CharField(max_length=20, null=True, blank=True)
    gender = db.CharField(max_length=10, null=True, blank=True)
    shipping_cost = db.FloatField(default=2000)
    is_visible= db.BooleanField(default=True)
    requested_delivery= db.BooleanField(default=False)
    rdate = db.DateTimeField(auto_now_add=True)
    delete_flag = db.BooleanField(default=False)
    shipping_info = db.JSONField(null=True, blank=True)

class Donators(db.Model):
    wishlist = db.ForeignKey(MySavedProduct, on_delete=db.CASCADE, related_name='donators')
    fullname=db.CharField(max_length=100)
    mobile=db.CharField(max_length=13)
    email=db.EmailField()
    amount=db.FloatField(null=True, blank=True)
    personal_message=db.TextField(null=True, blank=True)
    rdate=db.DateTimeField(auto_now_add=True)
    txn_ref=db.CharField(max_length=100, null=True, blank=True)
