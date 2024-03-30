from rest_framework import viewsets, permissions, exceptions, status
from .serializers import CustomUserSerializer, ProfileCustomUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


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
        return Response({"user": serializer.data})

    # def get_queryset(self):
    #     if self.request.user:
    #         user = get_user_model().objects.filter(pk=self.request.user.pk)
    #         if not user:
    #             raise exceptions.AuthenticationFailed("Пользователь не найден.")
    #         return user


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
