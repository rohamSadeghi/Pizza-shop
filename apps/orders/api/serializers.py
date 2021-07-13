from rest_framework import serializers

from apps.orders.models import OrderPizza
from apps.pizzas.api.serializers import PizzaSerializer


class OrderPizzaSerializer(serializers.ModelSerializer):
    pizza_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderPizza
        fields = ('id', 'pizza_details', 'pizza', 'description', 'price', 'is_paid', 'created_time')
        read_only_fields = ('id', 'created_time', 'price', 'is_paid')

    def get_pizza_details(self, order):
        return PizzaSerializer(order.pizza, context=self.context).data

    def update(self, instance, validated_data):
        pizza = validated_data['pizza']
        price = max((pizza.price - pizza.price_discount), 0)
        validated_data['price'] = price
        return super().update(instance, validated_data)
