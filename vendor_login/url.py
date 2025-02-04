from django.urls import path
from .views import vendor_login

urlpatterns = [
    path('login/', vendor_login, name='vendor_login'),
]
