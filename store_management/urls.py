from django.urls import path
from .views import *


urlpatterns = [
    # Create model paths
    path('add/new-food-product', view=AddFoodView.as_view(), name='add-new-food'),
    path('add/new-electronic-product', view=AddElecView.as_view(), name='add-new-electro'),
    path('add/new-forniture-product', view=AddFornView.as_view(), name='add-new-forni'),
    

    # Update model paths
    path('update/food-product/<int:pk>', view=EditFoodProduct.as_view(), name='food-update'),
    path('update/electronic-product/<int:pk>', view=EditElectroProduct.as_view(), name='electro-update'),
    path('update/forniture-product/<int:pk>', view=EditForniProduct.as_view(), name='forni-update')

]
