from collections.abc import Mapping
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from django.forms import ModelForm


class BaseProductForm(ModelForm):

    def save(self, commit: bool = True, *args, **kwargs) -> Any:
        self.instance.seller = self.data['seller']
        return super().save(commit, *args, **kwargs)


class FoodModelForm(BaseProductForm):

    class Meta:
        model = FoodProduct
        fields = ['name', 'price', 'is_local',
                  'is_available', 'img', 'description']
        help_texts = {
            'name': 'Name must be unique, between 10 and 50 characters',
            'price': "can't be 0€ or heigher than 999€",
            'is_available': 'Unmark this is you are currently out of stock',
            'is_local': 'If it was produced close to your location'
        }


class ElectronicModelForm(BaseProductForm):

    class Meta:
        model = ElectronicProduct
        fields = ['name', 'price', 'is_available', 'img', 'description']
        help_texts = {
            'name': 'Name must be unique, between 10 and 50 characters',
            'price': "can't be 0€ or heigher than 999€",
            'is_available': 'Unmark this is you are currently out of stock',
        }
