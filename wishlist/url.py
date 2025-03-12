from .views import wishlist, WishlistView
from django.urls import path


urlpatterns = [
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/api/', WishlistView.as_view(), name='wishlist_api'),
]