from functools import wraps
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from ..models import StoreUser, Seller
# from django.views import View


def unauthorized_user_redirect(view_method):

    def decorator(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_anonymous:
            redirect('home')
        else:
            return view_method(self, request, *args, **kwargs)

    return decorator


def user_is_anonymous(view_method):

    def decorator(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_anonymous:
            return view_method(self, request, *args, **kwargs)
        else:
            return redirect('home')

    return decorator


def admit_only_sellers(view_method):

    def decoretor(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_seller:
            return view_method(self, request, *args, **kwargs)
        else:
            raise PermissionDenied()
        
    return decoretor


def handle_img_from_form(view_method):
    """
    decorator function to handle the storate og the image loaded in a form
    note: remember to name the field "img" to proceed properly
    """

    def decorator(self, form: BaseModelForm, *args, **kwargs):
        instance = form.save(commit=False)
        if "img" in self.request.FILES:
            instance.img = self.request.FILES["img"]
            instance.save()
            return view_method(self, form, *args, **kwargs)
    return decorator



def add_info_to_form(key_name: str = 'store_user', edit_user_model: bool = False):
    """
    A decorator to add information to the form data, such as the user or other related data.

    key_name: The key under which the information will be added to the form data.
    edit_user_model: If True, edit the user model (e.g., set is_seller to True).
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, form: BaseModelForm, *args, **kwargs):
            data = form.data.copy()
            data[key_name] = self.request.user if key_name == 'store_user' else get_object_or_404(
                Seller, store_user_id= self.request.user.id)
            new_form = self.get_form()
            new_form.data = data
            if edit_user_model:
                user = get_object_or_404(StoreUser,  pk=self.request.user.id)
                user.is_seller = True
                user.save()
            return view_func(self, new_form, *args, **kwargs)
        return wrapper
    return decorator
