from django.urls import path, include
from rest_framework.routers import DefaultRouter

from botAPI.views import UserViewSet, health_check, SpaceViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'spaces', SpaceViewSet, basename='spaces')

urlpatterns = [
    path("", include(router.urls)),
    path("ping/", health_check),
]