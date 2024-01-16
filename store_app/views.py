from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View, DetailView, ListView
from django.views.generic.base import ContextMixin
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from store_management.models import BaseProduct
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import *
# Create your views here.

class HomeStore(TemplateView):
    template_name = 'store_app/index.html'


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['products'] = BaseProduct.objects.all()
        return context
    
class PreCart(View):
    pass

class ProductView(DetailView):
    template_name = 'store_app/product.html'
    model = BaseProduct
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
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
        context['product_type'] = actual_instance.__class__.__name__ # I'm not using this 
        context['update_url'] = update_link
        return context
    

class ProductsBySellerView(ListView):
    template_name = 'store_app/product_list.html'
    model = BaseProduct
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(seller_id=self.kwargs['pk'])


class MyCartView(LoginRequiredMixin, TemplateView):
    template_name = 'store_app/cart.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(client_id=self.request.user.id)
        cart.calculate_total_price()
        context['cart'] = cart
        return context


class MyWishView(LoginRequiredMixin, DetailView):
    model = WishList
    template_name = 'store_app/wish_list'
    

class RequirePostMixin:

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    


class BaseRequireView(RequirePostMixin, View):

    product = None

    def post(self, request: HttpRequest, *args, **kwargs):
        return redirect(self.get_success_url())
    
    def set_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        self.product = get_object_or_404(BaseProduct, pk=pk)

    def get_success_url(self, *args, **kwargs) -> str:
        return reverse('product', kwargs={'pk':self.product.pk})


class Add2Cart(LoginRequiredMixin, BaseRequireView):
    login_url = '/log-in'
    cart_item = None
    quantity = None
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        self.get_desired_quantity()
        self.set_cart_item()
        cart, created = Cart.objects.get_or_create(client_id=self.request.user.id)
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



class Add2Wish(BaseRequireView):

    def post(self,request: HttpRequest, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseRemove(LoginRequiredMixin, View):
    login_url = '/log-in'


class RemoveTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        return Cart.objects.get(client_id=self.request.user.id)


class RemoveFromCart(RemoveTest, BaseRemove):
    pass