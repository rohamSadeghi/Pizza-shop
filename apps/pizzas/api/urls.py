from django.urls import path, include
from rest_framework import routers

from apps.pizzas.api.views import PizzaViewSet

router = routers.SimpleRouter()
router.register(r'', PizzaViewSet, basename='pizzas')

urlpatterns = [
    path('', include(router.urls)),
]
