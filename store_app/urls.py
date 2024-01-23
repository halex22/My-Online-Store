from django.urls import path
from .views import *


urlpatterns = [
    path('', view=HomeStore.as_view(), name='home-store'),
    path('product/<int:pk>', view=ProductView.as_view(), name='product'),
    path('products/<str:name>-<int:pk>', view=ProductsBySellerView.as_view(), name='seller-products'),

    # Cart views
    path('my-cart', view=MyCartView.as_view(), name='cart'),
    path('add-product-to-cart/<int:pk>', view=Add2Cart.as_view(), name='add-2-cart'),
    path('remove-from-cart/<int:pk>', view=RemoveFromCart.as_view(), name='remove-from-cart'),

    # Wish List views
    path('my-wish-list/' , view=MyWishView.as_view(), name='wish-list'),
    path('add-product-to-wish-list/<int:pk>', view=Add2Wish.as_view(), name='add-2-wish'),
    path('remove-from-wish-list/<int:pk>', view=RemoveFromWishList.as_view(), name='remove-from-wish'),

    # Rating and Comment
    path('rate-and-comment/<int:pk>', view=AddRatingView.as_view(), name='rate-product'),
    path('fetch-comments/<int:pk>', view= FetchComments.as_view(), name='fetch-comments'),
]
