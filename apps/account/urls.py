from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
    TokenVerifyView,
)
from apps.account.serializers import AuthSerializer
from apps.account.views import PersonalAreaView

urlpatterns = [
    path('login/', TokenObtainSlidingView.as_view(serializer_class=AuthSerializer), name='token_obtain'),
    path('login/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_veify'),
    path('personal-area/me/', PersonalAreaView.as_view(), name='personal-area'),
]