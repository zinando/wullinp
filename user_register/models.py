from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    deleted = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255, default='user')

    def __str__(self):
        return self.user.username
