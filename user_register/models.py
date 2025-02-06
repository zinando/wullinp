from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    deleted = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255, default='user')
    # fields for vendors
    business_name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='_static/images/vendor_logos/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Platform approval

    def __str__(self):
        return self.user.username
