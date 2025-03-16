from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
import random
import string

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
    image_1_thumb_url = models.ImageField(upload_to='_static/images/products/1/thumb/', blank=True, null=True)
    image_2_thumb_url = models.ImageField(upload_to='_static/images/products/2/thumb/', blank=True, null=True)
    image_3_thumb_url = models.ImageField(upload_to='_static/images/products/3/thumb/', blank=True, null=True)
    image_4_thumb_url = models.ImageField(upload_to='_static/images/products/4/thumb/', blank=True, null=True)
    
    # field for cloud storage url
    image_1_cloud_url = models.URLField(blank=True, null=True)
    image_2_cloud_url = models.URLField(blank=True, null=True)
    image_3_cloud_url = models.URLField(blank=True, null=True)
    image_4_cloud_url = models.URLField(blank=True, null=True)
    image_1_cloud_thumb_url = models.URLField(blank=True, null=True)
    image_2_cloud_thumb_url = models.URLField(blank=True, null=True)
    image_3_cloud_thumb_url = models.URLField(blank=True, null=True)
    image_4_cloud_thumb_url = models.URLField(blank=True, null=True)
    image_1_pid = models.CharField(max_length=100, blank=True, null=True)
    image_2_pid = models.CharField(max_length=100, blank=True, null=True)
    image_3_pid = models.CharField(max_length=100, blank=True, null=True)
    image_4_pid = models.CharField(max_length=100, blank=True, null=True)
    image_1_thumb_pid = models.CharField(max_length=100, blank=True, null=True)
    image_2_thumb_pid = models.CharField(max_length=100, blank=True, null=True)
    image_3_thumb_pid = models.CharField(max_length=100, blank=True, null=True)
    image_4_thumb_pid = models.CharField(max_length=100, blank=True, null=True)
    
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    weight = models.FloatField(default=1) # weight in kg
    width = models.FloatField(default=0.025) # width in meters
    length = models.FloatField(default=0.025) #lenght in meters
    height = models.FloatField(default=0.025) # height in meters
    slug = models.SlugField(unique=True, blank=True)
    product_feature = models.JSONField(blank=True, null=True)
    cprice = models.DecimalField(max_digits=18, decimal_places=2, default=1.00)
    preprice = models.DecimalField(max_digits=18, decimal_places=2, default=2.00)
    min_quantity = models.IntegerField(default=1)
    vat = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    product_brand = models.IntegerField(blank=True, null=True)
    sizes = models.JSONField(blank=True, null=True)
    colors = models.JSONField(blank=True, null=True)
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
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]


    def __repr__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it doesn't exist
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Products.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        # save sku value if not exists
        if not self.sku:
            self.sku = f"{self.name[:3].upper()}-{generate_sku()}"
        super().save(*args, **kwargs)



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



def generate_sku():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
