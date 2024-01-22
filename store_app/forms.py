from django import forms
from django.forms import Textarea
from django.forms.fields import IntegerField, CharField   


class RateAndCommetForm(forms.Form):

    value = IntegerField(min_value=1, max_value=5, required=True)
    text = CharField(widget=Textarea, max_length=200, required=False)