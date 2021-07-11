from django.urls import path

from apps.accounts.api.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

]
