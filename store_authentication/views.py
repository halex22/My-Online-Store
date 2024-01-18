from typing import Any
from django.forms import BaseModelForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView
from store_management.aux_code import decorators

from django.shortcuts import redirect
from .models import *
from .forms import *


# Create your views here.
class MyBaseCreateView(CreateView):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def form_invalid(self, form):
        for field, errors in form.errors.as_data().items():
            print(f'field name: {field}')
            for v,error in enumerate(errors):
                print(f'{v +1}. {error}')
        return super().form_invalid(form)
    
class AuthenticationView(MyBaseCreateView):

    @decorators.user_is_anonymous
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    @decorators.user_is_anonymous
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    
class SignUp(AuthenticationView):
    template_name = 'store_auth/sign_up.html'
    model = StoreUser
    form_class = SingUpForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        login(**{'request':self.request, 'user': form.save()})
        return redirect('home-store')
    

class LogIn(LoginView):
    template_name = 'store_auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        next_param = self.request.GET.get('next')
        if next_param:
            return next_param
        else:
            return reverse('home-store')


class LogOut(LogoutView):
    next_page = reverse_lazy('home-store')


class BecomeSeller(MyBaseCreateView):
    template_name = 'store_auth/new_seller.html'
    model = Seller
    form_class = SellerForm

    success_url = reverse_lazy('home-store')

    @decorators.add_info_to_form(edit_user_model=True)
    def form_valid(self, form):
        return super().form_valid(form)
