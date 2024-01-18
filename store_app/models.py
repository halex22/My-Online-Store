from django.db import models
from store_management.models import *

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
        total = 0
        for item in self.products.all():
            total += item.total_cost
        return total

    def save(self, *args, **kwargs):
        # when the cart is crated it has no prodcuts
        # so only when it has some it will calculate the total_price
        
        try:
            # self.total_price = self.calculate_total_price()
            if self.products.all().__len__() == 0:
                self.total_price = 0
            else:
                self.total_price = self.calculate_total_price()

        except:
            pass
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
