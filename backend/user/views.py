from rest_framework import viewsets, permissions, exceptions, status
from .serializers import CustomUserSerializer, ProfileCustomUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

#from django.shortcuts import render_to_response
#from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json


@ensure_csrf_cookie
def auth_set_csrf_cookie(request):
    return JsonResponse({"details": "CSRF cookie set"})


@require_POST
def auth_login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    # добавить необходимые проверки
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"detail": "Success"})
    return JsonResponse({"detail": "Invalid credentials"}, status=400)


@require_POST
def auth_logout(request):
    logout(request)
    return JsonResponse({"detail": "Logout Successful"})



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileCustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileCustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        profile = self.get_queryset().get(pk=self.request.user.pk)
        serializer = self.get_serializer(profile)
        return Response({'user': serializer.data})

    # def get_queryset(self):
    #     if self.request.user:
    #         user = get_user_model().objects.filter(pk=self.request.user.pk)
    #         if not user:
    #             raise exceptions.AuthenticationFailed("Пользователь не найден.")
    #         return user


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
