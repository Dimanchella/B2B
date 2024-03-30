from django.urls import path, include
from .views import CustomUserViewSet, ProfileCustomUserViewSet, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"backend/api/v1/users", CustomUserViewSet, basename="users")
router.register(r"backend/api/v1/user", ProfileCustomUserViewSet, basename="user")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"backend/api/v1/user_logout/", LogoutView.as_view(), name="user_logout")
]


