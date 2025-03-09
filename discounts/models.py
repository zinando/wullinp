from django.db import models


# Create your models here.
class Discount(models.Model):
    code = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100)
    value = models.FloatField()
    minPurchase = models.FloatField()
    expiration = models.DateTimeField()
    usageLimit = models.IntegerField()
    usageCount = models.IntegerField()
    applicableProducts = models.JSONField()
    used_by = models.JSONField() # list of user ids
    applicableCategories = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'${self.code}-${self.value}-Expires: ${self.expiration.strftime("%d-%m-%Y")}'