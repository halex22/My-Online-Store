from typing import Any, Union, List
import json
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView, View
from django.views.generic.detail import BaseDetailView
from store_management.models import BaseProduct
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import *
from .my_classes.remove import MyRemoveView
from .my_classes.base import BaseRequireView
from .my_classes.object import MyObjectView
from .my_classes.rate import RateView

def get_actual_instance_price(instance: BaseProduct) -> str:
    """
    Takes an instance of the BaseProduct model and returns the 
    actual instance price as a string
    """
    actual_instance = None
    if hasattr(instance, 'foodproduct'):
            actual_instance = instance.foodproduct
    elif hasattr(instance, 'electronicproduct'):
        actual_instance = instance.electronicproduct
    else:
        actual_instance = instance.fornitureproduct
    return str(actual_instance.price)


class HomeStore(TemplateView):
    template_name = 'store_app/index_cat.html'
    model = BaseProduct
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['last_added'] = self.filter_products('added_date')
        context['most_voted'] = self.filter_products('n_votes')
        context['most_rated'] = self.filter_products('total_score')
        return context
    
    def filter_products(self, filter:str) -> QuerySet:
        filterd_products = cache.get(filter)

        if filterd_products is None:
            filterd_products = self.model.objects.all().order_by(f'-{filter}')[:3]
            cache.set(filter, filterd_products, timeout=600) # ten minutes    
        return filterd_products




class AllProducts(ListView):
    model = BaseProduct
    paginate_by = 6
    template_name = 'store_app/index.html'


class SearchProductsView(ListView):
    model = BaseProduct
    template_name = 'store_app/search_products.html'
    context_object_name = 'products'


        
    def get_user_query(self):
        q = self.request.get_full_path_info().split('=')[1]
        return q
    
    def get_queryset(self) -> QuerySet[Any]:
        user_query = self.get_user_query()
        return BaseProduct.objects.filter(
            Q(name__icontains= user_query) |
            Q(seller__name__icontains = user_query)
        )

class ProductView(DetailView):
    template_name = 'store_app/product.html'
    model = BaseProduct
    context_object_name = 'product'
    object = None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        instance = self.object
        actual_instance = None
        update_link = None
        if hasattr(instance, 'foodproduct'):
            actual_instance = instance.foodproduct
            update_link = 'food-update'
        elif hasattr(instance, 'electronicproduct'):
            actual_instance = instance.electronicproduct
            update_link = 'electro-update'
        else:
            actual_instance = instance.fornitureproduct
            update_link = 'forniture-update'
        context['product'] = actual_instance
        context['update_url'] = update_link
        context['is_in_wishlist'] = self.is_in_wishlist()
        
        context['rating'] = self.get_rating()
        return context

    def is_in_wishlist(self):
        if self.request.user.is_authenticated:
            wish, created = WishList.objects.get_or_create(
                client_id=self.request.user.id)
            return self.get_object() in wish.products.all()
        
    def get_rating(self) -> Union[Rating, None]:
        """If the product has been rated by the user it returns the instance of the `Rating` class
        else return `None` """
        try:
            return Rating.objects.get(client_id=self.request.user.id, product_id=self.object.pk)
        except:
            return None
        


class ProductsBySellerView(ListView):
    template_name = 'store_app/product_list.html'
    model = BaseProduct
    context_object_name = 'products'
    paginate_by = 6
    n_products = None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['seller_name'] = Seller.objects.get(pk=self.kwargs['pk']).name
        context['n_products'] = self.n_products
        
        return context

    def get_queryset(self) -> QuerySet[Any]:
        query = self.model.objects.filter(seller_id=self.kwargs['pk'])
        self.n_products = query.count()
        return query


# Object views
class MyCartView(MyObjectView):
    template_name = 'store_app/cart.html'
    model = Cart


class MyWishView(MyObjectView):
    template_name = 'store_app/wish_list.html'
    model = WishList
    context_object_name = 'wish_list'


# Add views
class Add2Cart(LoginRequiredMixin, BaseRequireView):
    login_url = reverse_lazy('log-in')
    cart_item = None
    quantity = None

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        self.get_desired_quantity()
        self.set_cart_item()
        cart, created = Cart.objects.get_or_create(
            client_id=self.request.user.id)
        cart.products.add(self.cart_item)
        cart.save()
        return super().post(request, *args, **kwargs)

    def get_desired_quantity(self, *args, **kwargs):
        self.quantity = int(self.request.POST['quantity'])

    def set_cart_item(self, *args, **kwargs):
        self.cart_item, created = CartItem.objects.get_or_create(
            product=self.product, customer=self.request.user
        )
        if created:
            self.cart_item.quantity += (self.quantity - 1)
        else:
            self.cart_item.quantity += self.quantity
        self.cart_item.save()


class Add2Wish(LoginRequiredMixin, BaseRequireView):
    login_url = reverse_lazy('log-in')
    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        list, created = WishList.objects.get_or_create(
            client_id=self.request.user.id)
        list.products.add(self.product)
        return super().post(request, *args, **kwargs)


# Remove views
class RemoveFromCart(MyRemoveView):
    """
    View that handles only POST request if the user is logged
    in and if the cart exits
    """
    test_model = Cart

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        parms = {'product_id':self.product.pk , 'customer_id':self.request.user.id}
        item = CartItem.objects.get(**parms)
        if item:
            self.test_model_object.products.remove(item)
            item.delete()
            self.test_model_object.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs) -> str:
        return reverse('cart')


class RemoveFromWishList(MyRemoveView):
    test_model = WishList

    def post(self, request: HttpRequest, *args, **kwargs):
        self.set_object()
        self.test_model_object.products.remove(self.product)
        return super().post(request, *args, **kwargs)


# Rating 
class AddRatingView(RateView):
    template_name = 'store_app/rating_and_comment.html'
    model = BaseProduct
    context_object_name = 'product'
    

class BaseJsonResponseView(View):
    response = None
    object_pk = None

    def no_data_response(self):
        self.response = json.dumps({'found': 0, 'data':{}})

    def get(self, *args, **kwargs):
        return JsonResponse(json.loads(self.response), safe=False)

class FetchComments(BaseJsonResponseView):

    def get(self, *args, **kwargs):
        self.object_pk = self.kwargs['pk']
        if self.has_comments():
            comments = Comment.objects.filter(product_id=self.object_pk)
            self.data_response(comments=comments)
        else:
            self.no_data_response()
        return super().get(self, *args, **kwargs)

    def data_response(self, comments: List[Comment]):
        response = {'found':1, 'data': {}}
        new_data = {}
        for comment in comments:
            new_data.update({f'{comment.pk}': {
                'name': comment.client.username.capitalize(),
                'date': comment.added_date.strftime("%Y-%m-%d %H:%M:%S"),
                'rating': comment.rating.value,
                'text': comment.text
            }})
        response['data'].update(new_data)
        self.response = json.dumps(response)

    def has_comments(self):
        return Comment.objects.filter(product_id=self.object_pk).exists()
    

class MoreProductFromSeller(BaseJsonResponseView):

    product_pk = None
    query_set = None

    def get(self, *args, **kwargs):
        self.set_pks()
        self.fetch_products()
        if self.query_set:
            self.data_response()
        else:
            self.no_data_response()
        return super().get(*args, **kwargs)

    def fetch_products(self):
        result = BaseProduct.objects.filter(seller_id=self.object_pk).exclude(pk=self.product_pk)
        if result.count() > 3:
            shuffled_queryset = result.order_by('?')
            self.query_set = shuffled_queryset[:3]
        else:
            self.query_set = result


    def set_pks(self):
        self.object_pk = self.kwargs['s_pk']
        self.product_pk = self.kwargs['p_pk']
    
    def data_response(self):
        response = {'found':1, 'data': {}}
        new_data = {}
        for product in self.query_set:
            new_data.update({f'{product.pk}': {
                'name': product.name,
                'img': product.img.url,
                'link': reverse('product', kwargs={'pk':product.pk}),
                'price': get_actual_instance_price(product)
            }})
        response['data'].update(new_data)
        self.response = json.dumps(response)


class GetCartNumber(View):

    client_id = None
    cart = None
    cart_len = None

    def get(self, *args, **kwargs):
        response = None
        if self.cart_exits():
            response = {'found':1 , 'number': self.cart_len}
        else:
            response = {'found': 0, 'number': 0}
        response = json.dumps(response)
        return JsonResponse(json.loads(response), safe=False)

    def cart_exits(self):
        self.client_id = self.request.user.id
        if Cart.objects.filter(client_id = self.client_id).exists():
            self.cart = Cart.objects.get(client_id = self.client_id)
            self.cart_len = self.cart.products.all().__len__()
            return True if self.cart_len > 0 else False



class OrdersView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('log-in')
    template_name = 'store_app/orders.html'
    model = Order
    context_object_name = 'orders'
    paginate_by = 8

    def get_queryset(self) -> QuerySet[Order]:
        return self.model.objects.filter(client_id= self.request.user.id).order_by('-added_date')


class OrderView(LoginRequiredMixin, BaseDetailView, TemplateView):
    template_name = 'store_app/order.html'
    login_url = reverse_lazy('log-in')
    model = Order