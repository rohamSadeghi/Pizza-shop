from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.orders.api.serializers import OrderPizzaSerializer
from apps.pizzas.api.serializers import PizzaSerializer, PizzaRateSerializer, PizzaCommentSerializer
from apps.pizzas.models import Pizza, PizzaComment


class PizzaViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """

        list:
            Return all pizza, ordered by most recently added.

        retrieve:
            Return a specific pizza detail.

        rate:
            Set a rate between 1 to 5 for a specific pizza.

        add_comment:
            Add a new comment to specific pizza.

        comments:
            Return all the comments for specific pizza.
    """
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.filter(is_enable=True).order_by('-created_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def get_serializer_class(self):
        # Note: this part is just for showing better documentation on swagger
        actions_serializer_map = {
            'rate': PizzaRateSerializer,
            'add_comment': PizzaCommentSerializer,
            'comments': PizzaCommentSerializer,
            'order': OrderPizzaSerializer
        }
        return actions_serializer_map.get(self.action, super().get_serializer_class())

    @action(detail=True, methods=['post'])
    def order(self, request, *args, **kwargs):
        pizza = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        price = max(pizza.price - pizza.price_discount, 0)
        serializer.save(user=request.user, pizza=pizza, price=price)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        pizza = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, pizza=pizza)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='add-comment')
    def add_comment(self, request, *args, **kwargs):
        pizza = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, pizza=pizza)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def comments(self, request, *args, **kwargs):
        pizza = self.get_object()
        qs = PizzaComment.approves.filter(pizza=pizza).order_by('-created_time')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
