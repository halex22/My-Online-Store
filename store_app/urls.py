from django.urls import path
from .views import *


urlpatterns = [
    path('', view=HomeStore.as_view(), name='home-store'),
    path('product/<int:pk>', view=ProductView.as_view(), name='product'),
    path('products/<str:name>-<int:pk>', view=ProductsBySellerView.as_view(), name='seller-products'),
    path('my-cart/<int:pk>', view=PreCart.as_view(), name='cart')
]
