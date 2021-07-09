from django.urls import path, include
from rest_framework import routers

from apps.accounts.api.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()

urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('', include(router.urls)),
]
