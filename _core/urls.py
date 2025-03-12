"""
URL configuration for _core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import home.views
from user_profile.views import update_profile, update_vendor_profile, change_user_password
from products.views import ProductView
from user_profile.views import fetch_states_data
from discounts.views import DiscountView


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', home.views.home, name='home'),
    path('user/', include('user_register.url'), name='user_register'),
    path('user/', include('wishlist.url')),
    path('user/', include('user_login.url'), name='user_login'),
    path('user/', include('user_logout.url'), name='user_logout'),
    path('vendor/', include('vendor_register.url'), name='vendor_register'),
    path('vendor/', include('vendor_dashboard.url'), name='vendor_dashboard'),
    path('vendor/', include('vendor_login.url'), name='vendor_login'),
    path('products/', ProductView, name='products_view'),
    path('user/', include('user_profile.url')),
    path('user/profile/update/', update_profile, name='update_user_profile'),
    path('vendor/profile/update/', update_vendor_profile, name='update_vendor_profile'),
    path('user/change_password/', change_user_password, name='change_user_password'),
    path('vendor/', include('products.url'), name='add_product'),
    path('vendor/', include('products.url'), name='vendor_products'),
    path('vendor/', include('products.url'), name='edit_product'),
    path('products/', include('products.url'), name='search_products'),
    path('checkout/', include('orders.url')),
    path('states_data/', fetch_states_data, name='fetch_states_data'),
    path('xvcdetdfgrtgasd/', DiscountView.as_view(), name='discounts'),
    # path('user/', include('user_profile.url'), name='update_user_profile'),
    # path('vendor/', include('user_profile.url'), name='update_vendor_profile'),

]
