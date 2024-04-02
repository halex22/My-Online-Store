import json
from typing import List

from django.db import models

from store_management.models import *


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




product_types = ['foodproduct', 'electronicproduct', 'fornitureproduct']


class CartItem(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(null=True, max_digits=5 ,decimal_places=2)
    customer = models.ForeignKey(StoreUser, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.get_product_price()
        return super().save(*args, **kwargs)
    
    def get_product_price(self):
        for _ in product_types:
            if hasattr(self.product, _):
                instance = getattr(self.product, _)
                return instance.price
            

class Cart(models.Model):
    client = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem, related_name = 'cart_items')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    def calculate_total_price(self):
        return sum(item.total_cost for item in self.products.all())
        # total = 0
        # for item in self.products.all():
        #     total += item.total_cost
        # return total

    def save(self, *args, **kwargs):

        if self.products.exists():
            self.total_price = self.calculate_total_price()
        else:
            self.total_price = 0

        super().save(*args, **kwargs)


class WishList(models.Model):
    client = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(BaseProduct, related_name = 'wished_products')


class BaseModel(models.Model):
    client = models.ForeignKey(StoreUser, on_delete= models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rating(BaseModel):
    value = models.PositiveIntegerField()
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='ratings')


class Comment(BaseModel):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='comments')
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True)


class Order(BaseModel):
    json_data = models.JSONField(null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    def make_data(self, products: List[CartItem]):
        data = {}
        for item in products:
            single_product_data = {
                item.pk: {
                    'name': item.product.name,
                    'price': get_actual_instance_price(item.product),
                    'quantity': item.quantity,
                    'total_cost': str(item.total_cost)
                }
            }
            data.update(single_product_data)
        self.json_data = json.loads(json.dumps(data))
        

