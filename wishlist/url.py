from .views import wishlist, WishlistView, wishlist_donators
from django.urls import path


urlpatterns = [
    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/api/', WishlistView.as_view(), name='wishlist_api'),
    path('wishlist/donators/', wishlist_donators, name='wishlist_donators'),
]