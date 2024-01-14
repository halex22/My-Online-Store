from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import Group, Permission

# Create your models here.
class StoreUser(AbstractUser):

    is_seller = models.BooleanField(default=False)
    card_number = models.IntegerField(blank=True, null=True)
    objects = UserManager()
    groups = models.ManyToManyField(
        Group, verbose_name=('groups'), blank=True,
        related_name='store_users',  # Add this line
        related_query_name='store_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='store_users_permissions',  # Add this line
        related_query_name='store_user_permission',
    )

    def __str__(self) -> str:
        return super().__str__()


class Seller(models.Model):

    name = models.CharField(max_length=50, unique=True)
    store_user = models.OneToOneField(
        StoreUser, on_delete=models.CASCADE, related_name="user", blank=True)
    
    def __str__(self) -> str:
        return self.name


class BaseProduct(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False, validators=[
                                MinLengthValidator(10, message='Name must contain at list 10 characters')
                            ])
    is_available = models.BooleanField(default=True)
    added_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    img = models.ImageField(upload_to="images", blank=True, null=True)
    rating = models.FloatField(default=0,
        validators=[
            MinValueValidator(0, message="The rating must be above 0"),
            MaxValueValidator(5, message="max rating value is 5")
        ])
    n_votes = models.IntegerField(default=0, null= True, blank=True, validators=[MinValueValidator(0, message='votes recived can not be lower than 0')])
    total_score = models.IntegerField(default=0, null= True, blank=True, validators=[MinValueValidator(0, message='total score can not be lower than 0')])
    slug = models.SlugField(blank=True)
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="product_seller")
    description = models.TextField(blank=True, null= True, max_length=200)

    def save(self, *args, **kwargs):
        self.slug = slugify(value=f"{self.seller}-{self.name}")
        self.modified_date = now()
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name



class FixedPriceProduct(BaseProduct):
    price = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2, validators=[
        MinValueValidator(0, message="price lower than 0 is not allowed"),
        MaxValueValidator(999, message="Price is over the current limit of 999€")
    ])

    class Meta:
        abstract = True


class BaseFoodProduct(FixedPriceProduct):
    is_local = models.BooleanField(default=True)
    exp_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class FoodProduct(BaseFoodProduct):
    """Class to represent a food"""


class ElectronicProduct(FixedPriceProduct):
    """Class to represent products like headphones or laptops"""



class FornitureProduct(FixedPriceProduct):
    """Class to represent products like chairs or beds"""
    # length width height