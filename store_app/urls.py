from django.urls import path
from .views import *


urlpatterns = [
    path('home', view=HomeStore.as_view(), name='home-store'),
    path('all-products', view=AllProducts.as_view(), name='all-products'),
    path('product/<int:pk>', view=ProductView.as_view(), name='product'),
    path('products/<str:name>-<int:pk>', view=ProductsBySellerView.as_view(), name='seller-products'),
    path('search/products', view=SearchProductsView.as_view(), name='search'),
    path('my-orders', view=OrdersView.as_view(), name='my-orders'),
    path('order/<int:pk>', view=OrderView.as_view(), name='order'), 

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
    path('fetch-more-product/<int:s_pk>/<int:p_pk>', view=MoreProductFromSeller.as_view(), name='more-products'),
    path('fetch-cart-products', view=GetCartNumber.as_view(), name='cart-number')

]
