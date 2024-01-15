from typing import Any
from django.forms import BaseModelForm
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .aux_code import decorators
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .models import *
from .forms import *


class BaseCreate(CreateView):

    @decorators.admit_only_sellers
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    @decorators.admit_only_sellers
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    @decorators.add_info_to_form(key_name='seller')
    def form_valid(self, form):
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


class MyBaseUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('log-in')


class SellerTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        return self.request.user.is_seller


class ProductOwnerTest(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.seller.store_user_id == self.request.user.id


class MyUpdateView(Seller, ProductOwnerTest, MyBaseUpdate):
    pass


class EditFoodProduct(MyUpdateView):
    template_name = 'store_management/update/food.html'
    model = FoodProduct
    form_class = FoodModelForm


class EditElectroProduct(MyUpdateView):
    template_name = 'store_management/update/electro.html'
    model = ElectronicProduct
    form_class = ElectronicModelForm
