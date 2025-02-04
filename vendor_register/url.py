from django.urls import path
from .views import vendor_register

urlpatterns = [
    path('register/', vendor_register, name='vendor_register'),
]
