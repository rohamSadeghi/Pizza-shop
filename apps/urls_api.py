from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="PIZZA SHOP APIs")

urlpatterns = [
    path('v1/accounts/', include("apps.accounts.api.urls")),
    path('v1/pizzas/', include("apps.pizzas.api.urls")),
    path('v1/orders/', include("apps.orders.api.urls")),

    path('v1/docs/', schema_view),
]
