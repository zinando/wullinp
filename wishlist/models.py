from django.db import models as db
from django.contrib.auth.models import User
from products.models import Products
from orders.models import Order

# Create your models here.
class MySavedProduct(db.Model):
    product = db.ForeignKey(Products, on_delete=db.CASCADE)
    user = db.ForeignKey(User, on_delete=db.CASCADE)
    order = db.ForeignKey(Order, on_delete=db.CASCADE, null=True, blank=True)
    is_visible= db.BooleanField(default=True)
    requested_delivery= db.BooleanField(default=False)
    rdate = db.DateTimeField(auto_now_add=True)

class Donators(db.Model):
    wishlist = db.ForeignKey(MySavedProduct, on_delete=db.CASCADE)
    fullname=db.CharField(max_length=100)
    mobile=db.CharField(max_length=13)
    email=db.EmailField()
