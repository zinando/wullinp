from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# create address model 
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    house_address = models.TextField()
    city = models.CharField(max_length=50)
    city_id = models.IntegerField(null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)
    lga_id = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100)
    state_id = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100)
    country_id = models.IntegerField(null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.house_address}'