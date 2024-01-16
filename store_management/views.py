from typing import Any
from django.forms import BaseModelForm
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from .aux_code import decorators
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .models import *
from .forms import *


class SellerTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        return self.request.user.is_seller


class BaseCreate(LoginRequiredMixin, SellerTest, CreateView):

    login_url = reverse_lazy('log-in')

    @decorators.add_info_to_form(key_name='seller')
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.success_url = reverse('product', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


# Create your views here.
class AddFoodView(BaseCreate):
    template_name = 'store_management/create/food.html'
    model = FoodProduct
    form_class = FoodModelForm


class AddElecView(BaseCreate):
    template_name = 'store_management/create/electro.html'
    model = ElectronicProduct
    form_class = ElectronicModelForm


# Update view section


class MyBaseUpdate(LoginRequiredMixin, UpdateView):

    login_url = reverse_lazy('log-in')


class ProductOwnerTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.seller.store_user_id == self.request.user.id


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
