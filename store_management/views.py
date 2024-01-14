from typing import Any
from django.forms import BaseModelForm
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView
from aux_code import decorators

from django.shortcuts import redirect
from .models import *
from .forms import *


# Create your views here.
