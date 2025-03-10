"""functions that are useful for the rest of the codebase"""
from django.contrib.auth.models import User
from user_register.models import Profile
from products.models import ProductCategory, Products
from discounts.models import Discount
from orders.models import Order, OrderItem, PGRequest
import uuid
import re
import os
from dotenv import load_dotenv

load_dotenv()

def check_if_username_is_phone_or_email(username):
    if '@' in username:
        return 'email'
    else:
        return 'phone'


def is_email_exists(email, user_id=None):
    if user_id:
        return User.objects.filter(email=email).exclude(id=user_id).exists()
    return User.objects.filter(email=email).exists()

def is_phone_exists(phone, user_id=None):
    if user_id:
        return Profile.objects.filter(phone=phone).exclude(user_id=user_id).exists()
    return Profile.objects.filter(phone=phone).exists()

def is_business_name_exists(business_name, user_id=None):
    if user_id:
        return Profile.objects.filter(business_name=business_name).exclude(id=user_id).exists()
    return Profile.objects.filter(business_name=business_name).exists()

def get_user_object(user_id):
    return User.objects.get(id=user_id)

def get_product_object(product_id):
    return Products.objects.get(id=product_id)

def sanitize_string(my_string):
    """Replaces invalid characters in the public_id with underscores"""
    return re.sub(r'[^a-zA-Z0-9/_-]', '_', my_string)

def check_if_category_has_products(category_id, min_products=1):
    """This function checks if a category has at least min_products"""
    category = ProductCategory.objects.get(id=category_id)
    return category.products.count() >= min_products

def generate_skux():
    return str(uuid.uuid4().hex[:10]).upper()

def calculate_shipping_cost(cart_items, user_address, delivery_method, delivery_type):
    # Define surcharges to match JS function
    base_cost = 2000
    weight_factor = 100
    international_surcharge = 2000
    non_lagos_surcharge = 1000
    express_delivery_surcharge = 1000
    home_delivery_surcharge = 1000

    # Calculate total weight
    total_weight = sum(item.product.weight * item.quantity for item in cart_items)

    # Convert country/state to lowercase for case-insensitive comparison
    country = user_address['country'].lower()
    state = user_address['state'].lower()

    # Apply surcharges based on user address
    if country != "nigeria":
        base_cost += international_surcharge
    elif state != "lagos":
        base_cost += non_lagos_surcharge

    # Apply surcharges based on delivery type and method
    if delivery_type == "express":
        base_cost += express_delivery_surcharge

    if delivery_method == "home":
        base_cost += home_delivery_surcharge

    # Add weight-based cost
    return base_cost + (total_weight * weight_factor)

def calculate_total_discount(cart_items, discount):
    total_discount = 0

    # If discount is not set or is empty, return 0
    if not discount:
        return 0

    # Check if minimum purchase amount is met
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if discount.minPurchase > total_price:
        return 0

    # Iterate over each product in the cart
    for item in cart_items:
        if not discount.applicableProducts or item.product.id in discount.applicableProducts:
            if discount.type == "percentage":
                total_discount += (item.product.price * item.quantity * discount.value) / 100
            elif discount.type == "fixed":
                total_discount += discount.value * item.quantity

    return total_discount



def verify_order(request, order_details):
    """This function verifies an order and returns the order details"""
    # Check if the order is empty 
    if not order_details:
        return {'status':0, 'order': order_details, 'message':'Order is empty', 'error':[]}
    # Confirm shipping cost
    shipping_cost = calculate_shipping_cost(request.user.cart_items, order_details['selectedDeliveryAddress'], order_details['deliveryMethod'], order_details['deliveryType'])
    print(shipping_cost)
    if order_details['shippingCost'] != shipping_cost:
        return {'status':0, 'order': order_details, 'message':'Shipping cost is incorrect', 'error':[]}
    # Confirm discount
    if order_details['discountData']['code']:
        try:
            fetched_discount = Discount.objects.get(code=order_details['discountData']['code'])
        except Discount.DoesNotExist:
            return {'status':0, 'order': order_details, 'message':'Discount code is invalid', 'error':[]}
        
        total_discount = calculate_total_discount(request.user.cart_items, fetched_discount)
        if order_details['discount'] != total_discount:
            return {'status':0, 'order': order_details, 'message':'Discount value is incorrect', 'error':[]}
    # Confirm total price
    total_price = sum(item.product.cprice * item.quantity for item in request.user.cart_items) + order_details['shippingCost'] - order_details['discount']
    if order_details['totalPrice'] != total_price:
        return {'status':0, 'order': order_details, 'message':'Total price is incorrect', 'error':[]}

    return {'status':1, 'order': order_details, 'message':'Order verified successfully', 'error':[]}

def prepare_order(request, order_details):
    """This function prepares an order for processing"""
    # Verify the order
    verification_result = verify_order(request, order_details)
    if verification_result['status'] == 0:
        return verification_result

    # Create the order
    order = Order.objects.create(
        user=request.user,
        delivery_address=order_details['selectedDeliveryAddress']['house_address'],
        delivery_method=order_details['deliveryMethod'],
        delivery_type=order_details['deliveryType'],
        shipping_cost=order_details['shippingCost'],
        discount=order_details['discount'],
        total=order_details['total'],
        sub_total=order_details['subTotal'],
        discount_code=order_details['discountData']['code'],
        delivery_city=order_details['selectedDeliveryAddress']['city'],
        delivery_state=order_details['selectedDeliveryAddress']['state'],
        delivery_country=order_details['selectedDeliveryAddress']['country'],
        payment_method= 'PAYSTACK' if order_details['paymentMethod'] == 'other' else 'WALLET',
    )

    # Add cart items to the order
    for item in request.user.cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            current_price=item.product.cprice,
            total_price=item.product.cprice * item.quantity,
            color=item.color,
            size=item.size,
            gender = item.gender,
            customer_approved = True,
            system_approved = True,
            customer_approved_date = item.created_at,
            system_approved_date = item.created_at
        )

    # Create a payment gateway request
    txn = PGRequest.objects.create(
        order=order,
        user=request.user,
        amount=order.total,
        customer_email=request.user.email,
    )

    # update order txn_ref with the txn referenceid
    order.txn_ref = txn.ref_id
    order.save()

    # Clear the user's cart
    #request.user.cart_items.clear()

    order_data = {
        'amount': order.total,
        'email': request.user.email,
        'reference': txn.ref_id,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'phone': request.user.profile.phone,
        'paystackPublicKey': os.getenv('PAYSTACK_PUBLIC_KEY'),
        'paymentPurpose': 'Order Payment',
    }

    return {'status':1, 'order': order_data, 'message':'Order processed successfully', 'error':[]}