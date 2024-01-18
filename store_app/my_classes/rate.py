from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic.detail import SingleObjectMixin, DetailView, BaseDetailView
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin


class CanRate(UserPassesTestMixin):
    """Mixin to check if the `user` has bought the product"""

    def test_func(self) -> bool | None:
        # latter change this to check if the user has bought the item
        return True


class BaseMixins(LoginRequiredMixin, CanRate):
    """Mixin that allows only user that are logged in and that 
    have bought the product"""
    login_url = 'log-in'


class BaseRateView(BaseMixins, BaseDetailView, TemplateResponseMixin):
    """
    Once the user is logged in and the test has been passed renders 
    an object and the desired template
    """

class RateView(BaseRateView):
    pass
