from django.urls import path
from .views import AddProductView, VendorProductsView, EditProductView, SearchView

urlpatterns = [
    #path('products/', ProductView, name='products_view'),
    path('products/add/', AddProductView, name='add_product'),
    path('products/', VendorProductsView, name='vendor_products'),
    path('products/edit/', EditProductView, name='edit_product'),
    path('search/', SearchView, name='search_products'),
]
