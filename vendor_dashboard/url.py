from django.urls import path
from .views import vendor_dashboard, orders

urlpatterns = [
    path('dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('orders/', orders, name='orders'),
]
