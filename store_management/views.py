from typing import Any
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .aux_code import decorators
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .models import *
from .forms import *


# common Mixins
class SellerTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        return self.request.user.is_seller


class ProductOwnerTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.seller.store_user_id == self.request.user.id


# Create views
    
class BaseCreate(LoginRequiredMixin, SellerTest, CreateView):

    login_url = reverse_lazy('log-in')

    @decorators.add_info_to_form(key_name='seller')
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.success_url = reverse('product', kwargs={'pk': self.object.pk})
        return super().form_valid(form)



class AddFoodView(BaseCreate):
    template_name = 'store_management/create/food.html'
    model = FoodProduct
    form_class = FoodModelForm


class AddElecView(BaseCreate):
    template_name = 'store_management/create/electro.html'
    model = ElectronicProduct
    form_class = ElectronicModelForm


class AddFornView(BaseCreate):
    template_name = 'store_management/create/forni.html'
    model = FornitureProduct
    form_class = ForniModelForm


# Update view section


class MyBaseUpdate(LoginRequiredMixin, UpdateView):

    login_url = reverse_lazy('log-in')


class MyUpdateView(Seller, ProductOwnerTest, MyBaseUpdate):

    @decorators.add_info_to_form(key_name='seller')
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.success_url = reverse('product', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class EditFoodProduct(MyUpdateView):
    template_name = 'store_management/update/food.html'
    model = FoodProduct
    form_class = FoodModelForm


class EditElectroProduct(MyUpdateView):
    template_name = 'store_management/update/electro.html'
    model = ElectronicProduct
    form_class = ElectronicModelForm


class EditForniProduct(MyUpdateView):
    template_name = 'store_management/update/forni.html'
    model = FornitureProduct
    form_class = ForniModelForm


# Delete view
class MyBaseDelete(LoginRequiredMixin, DeleteView):

    login_url = reverse_lazy('log-in')  


class MyDeleteView(SellerTest, MyBaseDelete):
    pass


class DeleteProductView(MyDeleteView):
    template_name = 'store_management/delete.html'
    model = BaseProduct
    context_object_name = 'product'

    def get_success_url(self) -> str:
        seller_name = self.request.user.seller.name
        seller_id = self.request.user.seller.id
        return reverse('seller-products', kwargs={'name':seller_name, 'pk':seller_id})