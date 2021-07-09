from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.orders.api.serializers import OrderPizzaSerializer
from apps.orders.models import OrderPizza


class OrderPizzaViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """

        list:
            Return all orders, ordered by most recently added.

        retrieve:
            Return a specific order detail.

        destroy:
            Delete a specific order.

    """
    serializer_class = OrderPizzaSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return OrderPizza.objects.filter(user=self.request.user, is_enable=True).order_by('-created_time')

    def perform_destroy(self, order):
        order.is_enable = False
        order.save()
