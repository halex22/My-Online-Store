from django.urls import path
from .views import *


urlpatterns = [
    path('', view=HomeStore.as_view(), name='home-store')
]
