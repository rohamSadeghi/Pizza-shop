from rest_framework import serializers

from apps.pizzas.models import Pizza, PizzaRate, PizzaComment


class PizzaSerializer(serializers.ModelSerializer):
    rating_avg = serializers.DecimalField(read_only=True, max_digits=2, decimal_places=1)
    rating_count = serializers.IntegerField(read_only=True)
    user_rate = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = ('id', 'name', 'price', 'price_discount', 'image',
                  'description', 'rating_count', 'rating_avg', 'user_rate')

    def get_user_rate(self, obj):
        user = self.context['request'].user

        if user.is_authenticated and self.context['view'].action == 'retrieve':
            try:
                return PizzaRate.objects.get(user=self.context['request'].user, pizza=obj).rate
            except PizzaRate.DoesNotExist:
                return


class PizzaRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaRate
        fields = ('id', 'rate', 'created_time')
        read_only_fields = ('id', 'created_time', )

    def create(self, validated_data):
        rate = validated_data.pop('rate')
        instance, _created = PizzaRate.objects.update_or_create(
            **validated_data,
            defaults={'rate': rate}
        )
        return instance


class PizzaCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PizzaComment
        fields = ('id', 'content')
        read_only_fields = ('id', 'created_time', )
