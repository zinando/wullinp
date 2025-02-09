from django.urls import path
from .views import user_profile #, update_profile, update_vendor_profile

urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
    # path('profile/update/', update_profile, name='update_user_profile'),
    # path('profile/update/', update_vendor_profile, name='update_vendor_profile'),
]
