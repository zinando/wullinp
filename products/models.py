from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
#import ENUM
from enum import Enum

# Create your models here.
class Products(models.Model):
    # create a many to one relationship with the user model
    store = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=1)
    description = models.TextField()
    image_1_url = models.ImageField(upload_to='_static/images/products/1/', blank=True, null=True)
    image_2_url = models.ImageField(upload_to='_static/images/products/2/', blank=True, null=True)
    image_3_url = models.ImageField(upload_to='_static/images/products/3/', blank=True, null=True)
    image_4_url = models.ImageField(upload_to='_static/images/products/4/', blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    product_feature = models.JSONField(blank=True, null=True)
    cprice = models.DecimalField(max_digits=18, decimal_places=2, default=1.00)
    preprice = models.DecimalField(max_digits=18, decimal_places=2, default=2.00)
    min_quantity = models.IntegerField(default=1)
    vat = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    product_brand = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=False, null=False)
    featured = models.BooleanField(default=False)
    product_status = models.CharField(max_length=50, blank=False, null=False, default='inactive') # active, inactive, draft
    admin_action = models.CharField(max_length=50, blank=False, null=False, default='inactive') # active, inactive
    views = models.IntegerField(default=0) # number of views
    shipping_params = models.JSONField(blank=True, null=True)
    buyer_notes = models.TextField(blank=True, null=True)
    rdate = models.DateTimeField(auto_now_add=True)
    moddate = models.DateTimeField(auto_now=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    reviewed = models.BooleanField(default=False)
    admin_act_reason = models.TextField(blank=True, null=True)

    def __repr__(self):
        return self.name



class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
