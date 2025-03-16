from django.urls import path
from .views import user_profile, user_addresses, user_wallet, user_dashboard

urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
    path('addresses/', user_addresses, name='user_addresses'),
    path('wallet/', user_wallet, name='user_wallet'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    # path('profile/update/', update_profile, name='update_user_profile'),
    # path('profile/update/', update_vendor_profile, name='update_vendor_profile'),
]
