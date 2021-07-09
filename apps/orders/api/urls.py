from django.urls import path, include
from rest_framework import routers

from apps.orders.api.views import OrderPizzaViewSet

router = routers.SimpleRouter()
router.register(r'', OrderPizzaViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
