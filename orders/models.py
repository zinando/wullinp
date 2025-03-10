from django.db import models
from django.contrib.auth.models import User
from products.models import Products
import uuid

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
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    class OrderType(models.TextChoices):
        CHECKOUT = "CHECKOUT", "Checkout"
        WISHLIST = "WISHLIST", "Wishlist"
    class PaymentMethod(models.TextChoices):
        PAYSTACK = "PAYSTACK", "Paystack"
        FLUTTERWAVE = "FLUTTERWAVE", "Flutterwave"
        STRIPE = "STRIPE", "Stripe"
        RAVE = "RAVE", "Rave"
        PAYPAL = "PAYPAL", "Paypal"
        BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
        CASH_ON_DELIVERY = "CASH_ON_DELIVERY", "Cash on Delivery"
        WALLET = "WALLET", "Wallet"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    sub_total = models.FloatField(default=0)
    total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)
    payment_status = models.CharField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING, max_length=20)
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    delivery_city = models.CharField(max_length=50, null=True, blank=True)
    delivery_state = models.CharField(max_length=50, null=True, blank=True)
    delivery_country = models.CharField(max_length=50, null=True, blank=True)
    delivery_method = models.CharField(max_length=50, null=True, blank=True)
    delivery_type = models.CharField(max_length=50, null=True, blank=True)
    order_status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=20)
    txn_ref = models.CharField(max_length=100, null=True, blank=True)
    order_type = models.CharField(choices=OrderType.choices, default=OrderType.CHECKOUT, max_length=20)
    redeem_requested = models.BooleanField(default=False)
    redeem_code = models.CharField(max_length=50, null=True, blank=True)
    payment_method = models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.PAYSTACK, max_length=20)
    delivery_date = models.DateField(null=True, blank=True)
    delete_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.total_price}'
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'ORD-{str(self.user.id)}-{str(self.created_at.strftime("%Y%m%d%H%M%S"))}'
        super().save(*args, **kwargs)

# create order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_items')
    vendor_approved = models.BooleanField(default=False)
    vendor_approved_date = models.DateTimeField(null=True, blank=True)
    system_approved = models.BooleanField(default=False)
    system_approved_date = models.DateTimeField(null=True, blank=True)
    customer_approved = models.BooleanField(default=False)
    customer_approved_date = models.DateTimeField(null=True, blank=True)
    current_price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0)
    cash_back = models.FloatField(default=0)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    delete_flag = models.BooleanField(default=False)
    hold_vendor_payment = models.BooleanField(default=False)
    vendor_paid_flag = models.BooleanField(default=False)
    admin_over_ride = models.BooleanField(default=False)
    admin_overide_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_overide_user', null=True, blank=True)
    waybillnumber = models.CharField(max_length=50, null=True, blank=True)
    ship_cost = models.FloatField(default=0)
    out_of_stock_on_purchase = models.BooleanField(default=False)
    redeem_requested= models.BooleanField(default=False)
    vendor_marked_delivered = models.BooleanField(default=False)
    vendor_marked_delivered_date = models.DateTimeField(null=True, blank=True)
    vendor_marked_delivered_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_marked_delivered_user', null=True, blank=True)
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
    class TransactionType(models.TextChoices):
        DONATION = "DONATION", "Donation"
        CHECKOUT = "CHECKOUT", "Checkout"
    class ResponseStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    user_card = models.ForeignKey(UserCards, on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)
    amount = models.FloatField( default=0)
    ref_id = models.CharField( max_length=100, null=True, blank=True)
    txn_type = models.CharField(choices=TransactionType.choices, default=TransactionType.CHECKOUT, max_length=20)
    customer_email = models.EmailField()
    hook_res_id = models.CharField( max_length=50, null=True, blank=True)
    res_status = models.CharField(choices=ResponseStatus.choices, default=ResponseStatus.PENDING, max_length=20)
    callback_body = models.JSONField(null=True, blank=True)
    txn_verified = models.BooleanField(default=False)
    hook_check = models.BooleanField(default=False)
    reqhash = models.CharField( max_length=50, null=True, blank=True)
    contribute_code= models.CharField( max_length=50, null=True, blank=True)
    personal_message= models.TextField(null=True, blank=True)
    delete_flag = models.BooleanField(default=False)
    rdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.amount} on {self.rdate.strftime("%d-%M-%Y %HH:%MM:%SS")}'
    
    def save(self, *args, **kwargs):
        if not self.ref_id:
            # generate a unique refid with uuid
            self.ref_id = f'REF-{self.user.id}-{str(uuid.uuid4().hex[:8].upper())}'
        super().save(*args, **kwargs)

class PaystackHook(models.Model):
    resp = models.TextField()
    hook_res_id = models.CharField(max_length=50, null=True, blank=True)
    transactionid = models.CharField( max_length=100)
    hookdate = models.DateTimeField(auto_now_add=True)
    hook_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.transactionid} - {self.hookdate.strftime("%d-%M-%Y %HH:%MM:%SS")}- {self.resp}'

