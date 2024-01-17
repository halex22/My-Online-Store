from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
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


class BaseSingleObjectMixin(LoginRequiredMixin, SingleObjectMixin):
    """Mix in that combines `LoginRequiredMixn` and fetches the instance of the model
    using `get_or_create` query in the `get_object` method"""

    login_url = '/log-in'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        instance, created = self.model.objects.get_or_create(client_id=self.request.user.id)
        return instance
    

class MyObjectView(BaseSingleObjectMixin, TemplateView):
    """My view to get the `Cart` and `Wish List` objects"""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class MyCartView(MyObjectView):
    template_name = 'store_app/cart.html'
    model = Cart


class MyWishView(MyObjectView):
    template_name = 'store_app/wish_list.html'
    model = WishList
    context_object_name = 'wish_list'
    

class RequirePostMixin:
    """Mixin that allows only POST requests"""

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    


class BaseRequireView(RequirePostMixin, View):
    """
    View that only accepts POST requests. Call the set_object method inside the post mothod at first place
    """

    product = None
    redirect_url = None

    def post(self, request: HttpRequest, *args, **kwargs):
        """Call the set_object first to avoid errorss"""
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
        self.set_object()
        list, created = WishList.objects.get_or_create(client_id=self.request.user.id)
        # list.products.add(self.product)
        return super().post(request, *args, **kwargs)


class BaseRemove(LoginRequiredMixin, BaseRequireView):
    """View that accepts only POST request if the user is authenticated"""
    login_url = '/log-in'


class RemoveTest(UserPassesTestMixin):
    """Mixin that checks if the cart exists"""
    def test_func(self) -> bool | None:
        return Cart.objects.get(client_id=self.request.user.id)


class RemoveFromCart(RemoveTest, BaseRemove):
    """
    View that handles only POST request if the user is logged
    in and if the cart exits
    """
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        print(self.product)
        item = CartItem.objects.get(product_id=self.product.pk)
        if item:
            cart = Cart.objects.get(client_id=self.request.user.id)
            cart.products.remove(item)
            item.delete()
            cart.save()
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self, *args, **kwargs) -> str:
        return reverse('cart')
