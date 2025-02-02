from .views import wishlist
from django.urls import path

urlpatterns = [
    path('wishlist/', wishlist, name='wishlist'),
]