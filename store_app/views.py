from typing import Any
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, View
from store_management.models import BaseProduct
# Create your views here.

class HomeStore(TemplateView):
    template_name = 'store_app/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['products'] = BaseProduct.objects.all()
        print(context['products'])
        return context
