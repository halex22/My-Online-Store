from .base import BaseRequireView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class BaseRemove(LoginRequiredMixin, BaseRequireView):
    """View that accepts only POST request if the user is authenticated"""
    login_url = '/log-in'


class AccessTestMixin(UserPassesTestMixin):
    """Mixin that checks if the `Cart` or `WishList` exists.
    Set the `test_model` params when extending this class.
    If the objects exits it is passed to the `test_model_object` param
    """
    test_model = None
    test_model_object = None

    def test_func(self) -> bool | None:
        id = self.request.user.id
        try:
            self.test_model_object = self.test_model.objects.get(client_id=id)
            return True
        except:
            return False


class MyRemoveView(AccessTestMixin, BaseRemove):
    """"""
