from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, View
# Create your views here.

class HomeStore(TemplateView):
    template_name = 'store_app/index.html'

