from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.urls import reverse
from store_management.models import BaseProduct



class RequirePostMixin:
    """Mixin that allows only `POST` requests"""

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

class BaseRequireView(RequirePostMixin, View):
    """
    View that only accepts `POST` requests. Call the `set_object` method inside the post mothod at first place
    """

    product = None
    redirect_url = None

    def post(self, request: HttpRequest, *args, **kwargs):
        """Call the `set_object` first to avoid errorss"""
        return redirect(self.get_success_url())

    def set_object(self, *args, **kwargs) -> BaseProduct:
        """
        Fetches the product instance using the `pk`
        :return: `BaseProduct` object
        """
        pk = self.kwargs['pk']
        self.product = get_object_or_404(BaseProduct, pk=pk)

    def get_success_url(self, *args, **kwargs) -> str:
        return reverse('product', kwargs={'pk': self.product.pk})
