from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm


class FoodModelForm(ModelForm):

    class Meta:
        model = FoodProduct
        exclude = ['seller']
