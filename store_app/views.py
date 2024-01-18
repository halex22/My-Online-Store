from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from store_management.models import BaseProduct
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import *
from .my_classes.remove import MyRemoveView
from .my_classes.base import BaseRequireView
from .my_classes.object import MyObjectView
from .my_classes.rate import BaseRateView

class HomeStore(TemplateView):
    template_name = 'store_app/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['products'] = BaseProduct.objects.all()
        return context


class ProductView(DetailView):
    template_name = 'store_app/product.html'
    model = BaseProduct
    context_object_name = 'product'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        actual_instance = None
        update_link = None
        if hasattr(instance, 'foodproduct'):
            actual_instance = instance.foodproduct
            update_link = 'food-update'
        elif hasattr(instance, 'electronicproduct'):
            actual_instance = instance.electronicproduct
            update_link = 'electro-update'
        else:
            actual_instance = instance.fornitureproduct
            update_link = 'forniture-update'
        context['product'] = actual_instance
        # I'm not using this
        context['product_type'] = actual_instance.__class__.__name__
        context['update_url'] = update_link
        context['is_in_wishlist'] = self.is_in_wishlist()
        return context

    def is_in_wishlist(self):
        if self.request.user.is_authenticated:
            wish, created = WishList.objects.get_or_create(
                client_id=self.request.user.id)
            return self.get_object() in wish.products.all()


class ProductsBySellerView(ListView):
    template_name = 'store_app/product_list.html'
    model = BaseProduct
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(seller_id=self.kwargs['pk'])


# Object views
class MyCartView(MyObjectView):
    template_name = 'store_app/cart.html'
    model = Cart


class MyWishView(MyObjectView):
    template_name = 'store_app/wish_list.html'
    model = WishList
    context_object_name = 'wish_list'


# Add views
class Add2Cart(LoginRequiredMixin, BaseRequireView):
    login_url = '/log-in'
    cart_item = None
    quantity = None

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        self.get_desired_quantity()
        self.set_cart_item()
        cart, created = Cart.objects.get_or_create(
            client_id=self.request.user.id)
        cart.products.add(self.cart_item)
        cart.save()
        return super().post(request, *args, **kwargs)

    def get_desired_quantity(self, *args, **kwargs):
        self.quantity = int(self.request.POST['quantity'])

    def set_cart_item(self, *args, **kwargs):
        self.cart_item, created = CartItem.objects.get_or_create(
            product=self.product, customer=self.request.user
        )
        if created:
            self.cart_item.quantity += (self.quantity - 1)
        else:
            self.cart_item.quantity += self.quantity
        self.cart_item.save()


class Add2Wish(LoginRequiredMixin, BaseRequireView):

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        list, created = WishList.objects.get_or_create(
            client_id=self.request.user.id)
        list.products.add(self.product)
        return super().post(request, *args, **kwargs)


# Remove views
class RemoveFromCart(MyRemoveView):
    """
    View that handles only POST request if the user is logged
    in and if the cart exits
    """
    test_model = Cart

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        item = CartItem.objects.get(product_id=self.product.pk)
        if item:
            self.test_model_object.products.remove(item)
            item.delete()
            self.test_model_object.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs) -> str:
        return reverse('cart')


class RemoveFromWishList(MyRemoveView):
    test_model = WishList

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        self.test_model_object.products.remove(self.product)
        return super().post(request, *args, **kwargs)


# Rating 
class AddRatingView(BaseRateView):
    template_name = 'store_app/rating_and_comment.html'
    model = BaseProduct
    context_object_name = 'product'
