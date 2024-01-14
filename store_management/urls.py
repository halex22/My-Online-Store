from django.urls import path
from .views import *

urlpatterns = [
    # Create model paths
    path('add/new-food-product', view=AddFoodView.as_view(), name='add-new-food'),
]
