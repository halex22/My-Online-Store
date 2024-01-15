from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, View, DetailView
from store_management.models import BaseProduct
# Create your views here.

class HomeStore(TemplateView):
    template_name = 'store_app/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['products'] = BaseProduct.objects.all()
        print(context['products'])
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
        context['product'] = actual_instance
        context['product_type'] = actual_instance.__class__.__name__
        context['update_url'] = update_link
        return context
    

class ProductsBySellerView(TemplateView):
    template_name = 'store_app/product_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['products'] = BaseProduct.objects.filter(seller_id=self.kwargs['pk'])
        return context
    