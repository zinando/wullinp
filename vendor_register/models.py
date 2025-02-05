from django.contrib.auth.models import AbstractUser
from django.db import models 

# Create your models here.
class Vendor(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group', related_name='vendor_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='vendor_permissions', blank=True
    )
    business_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='_static/images/vendor_logos/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Platform approval

    def __str__(self):
        return self.business_name
