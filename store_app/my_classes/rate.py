from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models.base import Model as Model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateResponseMixin
from ..forms import RateAndCommetForm
from ..models import Rating, Comment


class CanRate(UserPassesTestMixin):
    """Mixin to check if the `user` has bought the product"""

    def test_func(self) -> bool | None:
        # latter change this to check if the user has bought the item
        has_bought_item = True
        new_date = True
        return all((has_bought_item, new_date))


class BaseMixins(LoginRequiredMixin, CanRate):
    """Mixin that allows only user that are logged in and that 
    have bought the product"""
    login_url = 'log-in'


class BaseRateView(BaseMixins, BaseDetailView, TemplateResponseMixin):
    """
    Once the user is logged in and the test has been passed renders 
    an object and the desired template
    """


class RateCommentMixin(FormMixin):
    form_class = RateAndCommetForm


class RateView(BaseRateView, RateCommentMixin):

    product = None

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form=form)
        else:
            return self.form_invalid(form=form)

    def form_invalid(self, form: Any) -> HttpResponse:
        errors = form.errors.as_data()
        print(errors)
        return redirect('rate-product', pk=3)

    def form_valid(self, form: Any) -> HttpResponse:
        self.product = self.get_object()
        data = form.data.copy()
        base_kwargs = self.get_object_and_user()
        base_kwargs.update({'value': data['value']})
        rating = Rating(**base_kwargs)
        rating.save()
        if data['text'] != '':
            base_kwargs.pop('value')
            base_kwargs.update({'text': data['text'], 'rating_id':rating.pk})
            commet = Comment(**base_kwargs)
            commet.save()
        self.product.update_rating(int(data['value']))
        return redirect('product', pk=self.product.pk)

    def get_object_and_user(self):
        return {'client_id': self.request.user.id, 'product_id': self.product.pk}
    
    # def update_product_rating(self, rating:int):
    #     self.update_product_rating

