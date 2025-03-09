from .views import checkoutView, modifyCartItem
from django.urls import path

urlpatterns = [
    path('checkout/', checkoutView, name='checkout'),
    path('modify-cart/', modifyCartItem, name='modify-cart'),
]