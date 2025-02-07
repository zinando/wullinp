from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    # create a many to one relationship with the user model
    store = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField()
    image_1_url = models.ImageField(upload_to='_static/images/products/1/', blank=True, null=True)
    image_2_url = models.ImageField(upload_to='_static/images/products/2/', blank=True, null=True)
    image_3_url = models.ImageField(upload_to='_static/images/products/3/', blank=True, null=True)
    image_4_url = models.ImageField(upload_to='_static/images/products/4/', blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ProductCategory(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
