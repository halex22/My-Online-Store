from django.urls import path
from .views import *


urlpatterns = [
    path('', view=HomeStore.as_view(), name='home-store'),
    path('product/<int:pk>', view=ProductView.as_view(), name='product'),
    path('products/<str:name>-<int:pk>', view=ProductsBySellerView.as_view(), name='seller-products'),

    # Cart views
    path('my-cart/<int:pk>', view=MyCartView.as_view(), name='cart'),
    path('add-product-to-cart/<int:pk>', view=Add2Cart.as_view(), name='add-2-cart'),

    # Wish List views
    path('my-wish-list/<int:pk>' , view=MyWishView.as_view(), name='wish-list'),
    path('add-product-to-wish-list/<int:pk>', view=Add2Wish.as_view(), name='add-2-wish'),

]
