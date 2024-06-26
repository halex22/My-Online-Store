from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up', view=SignUp.as_view(), name='sign-up'),
    path('log-in', view=LogIn.as_view(), name='log-in'),
    path('log-out', view=LogOut.as_view(), name='log-out'),
    path('become-a-seller', view=BecomeSeller.as_view(), name='become-seller')
]
