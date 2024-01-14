from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .models import *

from django.utils.html import format_html, format_html_join


pass_help = [
    # 'Your password can’t be too similar to your other personal information.',
    'Your password must contain at least 8 characters.',
    'Your password can’t be a commonly used password.',
    'Your password can’t be entirely numeric.'
]

class SingUpForm(UserCreationForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        t = format_html_join('', '<li class="text-sm text-gray-500 dark:text-gray-400">{}</li>',
                             ((help_text,) for help_text in pass_help))
        self.fields['password1'].__setattr__(
            'help_text', format_html('<ul>{}</ul>', t))

    class Meta:
        model = StoreUser

        fields = ("username",)