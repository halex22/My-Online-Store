from django.forms import Form, Textarea
from django.forms.fields import IntegerField, CharField


class RateAndCommetForm(Form):

    value = IntegerField(min_value=1, max_value=5)
    text = CharField(widget=Textarea)