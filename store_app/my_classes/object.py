from typing import Any
from django.db.models.base import Model as Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView


class BaseSingleObjectMixin(LoginRequiredMixin, SingleObjectMixin):
    """Mix in that combines `LoginRequiredMixn` and fetches the instance of the model
    using `get_or_create` query in the `get_object` method"""

    login_url = '/log-in'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        instance, created = self.model.objects.get_or_create(
            client_id=self.request.user.id)
        return instance
    
    
class MyObjectView(BaseSingleObjectMixin, TemplateView):
    """My view to get the `Cart` and `Wish List` objects"""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)