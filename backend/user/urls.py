from django.urls import path, include
from .views import CustomUserViewSet, ProfileCustomUserViewSet, LogoutView
from .views import auth_set_csrf_cookie, auth_login, auth_logout
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"backend/api/v1/users", CustomUserViewSet, basename="users")
router.register(r"backend/api/v1/user", ProfileCustomUserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
    #path(r"backend/api/v1/user_logout/", LogoutView.as_view(), name="user_logout"),
    path("auth/csrf/", auth_set_csrf_cookie),
    path("auth/login/", auth_login),
    path("auth/logout/", auth_logout)
]



