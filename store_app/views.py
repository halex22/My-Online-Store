from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import HttpResponse, redirect
from django.views.generic import TemplateView, View, DetailView, ListView
from django.views.generic.base import ContextMixin
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from store_management.models import BaseProduct
from django.contrib.auth.mixins import LoginRequiredMixin
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


class MyCartView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'store_app/cart.html'


class MyWishView(LoginRequiredMixin, DetailView):
    model = WishList
    template_name = 'store_app/wish_list'
    

class RequirePostMixin:

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    


class BaseAdd(RequirePostMixin, View):

    product = None

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        return redirect(self.get_success_url())
    
    def set_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        self.product = get_object_or_404(BaseProduct, pk=pk)

    def get_success_url(self, *args, **kwargs) -> str:
        return reverse('product', kwargs={'pk':self.product.pk})


class Add2Cart(BaseAdd):
    
    def post(self, request: HttpRequest, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class Add2Wish(BaseAdd):

    def post(self,request: HttpRequest, *args, **kwargs):
        return super().post(request, *args, **kwargs)