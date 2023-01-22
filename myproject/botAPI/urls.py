from django.urls import path, include
from rest_framework.routers import DefaultRouter

from botAPI.views import UserViewSet, health_check, SpaceViewSet, CategoryViewSet, ReferralCodeViewSet, SpendingViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'spaces', SpaceViewSet, basename='spaces')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'codes', ReferralCodeViewSet, basename='codes')
router.register(r'expenses', SpendingViewSet, basename='expenses')

urlpatterns = [
    path("", include(router.urls)),
    path("ping/", health_check),
]