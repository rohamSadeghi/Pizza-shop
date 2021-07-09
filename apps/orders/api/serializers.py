from rest_framework import serializers

from apps.orders.models import OrderPizza
from apps.pizzas.api.serializers import PizzaSerializer


class OrderPizzaSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(read_only=True)

    class Meta:
        model = OrderPizza
        fields = ('id', 'pizza', 'description', 'price', 'is_paid', 'created_time')
        read_only_fields = ('id', 'created_time', 'price', 'is_paid')
