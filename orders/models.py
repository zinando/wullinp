from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.
#create cart model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    total_discount = models.FloatField(default=0)
    shipping = models.FloatField(default=0)
    payment_status = models.TextChoices('PaymentStatus', 'PENDING PAID FAILED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.total_price}'

# create order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

class UserCards(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debit_cards')
    card_token = models.CharField(unique=True)
    card_name = models.CharField( max_length=50)
    exp_month = models.CharField( max_length=7)
    exp_year = models.CharField( max_length=7)
    first6 = models.CharField( max_length=7)
    bank = models.CharField( max_length=50)
    is_valid = models.BooleanField(default=True)
    is_disabled= models.BooleanField(default=False)
    rdate= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.card_name
class PGRequest(models.Model): #payment gateway request log
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    user_card = models.ForeignKey(UserCards, on_delete=models.CASCADE, related_name="transactions")
    amount = models.FloatField( default=0)
    refid = models.CharField( max_length=100, null=True, blank=True)
    txn_type = models.CharField( max_length=50, null=True, blank=True)
    customeremail = models.EmailField()
    hook_res_id = models.CharField( max_length=50, null=True, blank=True)
    res_status = models.CharField( max_length=50, null=True, blank=True)
    callback_body = models.TextField()
    hook_verified = models.BooleanField(default=False)
    hook_check = models.BooleanField(default=False)
    reqhash = models.CharField( max_length=50, null=True, blank=True)
    contribute_code= models.CharField( max_length=50, null=True, blank=True)
    personal_message= models.TextField()
    rdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.amount} on {self.rdate.strftime("%d-%M-%Y %HH:%MM:%SS")}'

class PaystackHook(models.Model):
    resp = models.TextField()
    hook_res_id = models.CharField(max_length=50, null=True, blank=True)
    transactionid = models.CharField( max_length=100)
    hookdate = models.DateTimeField(auto_now_add=True)
    hook_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.transactionid} - {self.hookdate.strftime("%d-%M-%Y %HH:%MM:%SS")}- {self.resp}'

