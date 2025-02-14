from django.urls import path
from .views import AddProductView

urlpatterns = [
    #path('products/', ProductView, name='products_view'),
    path('products/add/', AddProductView, name='add_product'),
]
