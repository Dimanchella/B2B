from uuid import uuid4
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid4)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "contractor", "full_name")

    def create(self, validated_data):
        user = super().create(validated_data)
        if validated_data.get("password"):
            password = validated_data.get("password")
        else:
            password = user.generate_random_password()
        user.set_password(password)
        user.save()
        # user.send_welcome_email(password) # XXX
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        have_changes = False

        if validated_data.get("password"):
            user.set_password(validated_data.get("password"))
            have_changes = True
        if validated_data.get("contractor"):
            have_changes = True
        if validated_data.get("email"):
            have_changes = True

        if have_changes:
            user.save()
        return user


class ProfileCustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("full_name", "username", "contractor",)


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["lifetime"] = str(refresh.access_token.lifetime.total_seconds())
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):
    
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)
            data["lifetime"] = str(refresh.access_token.lifetime.total_seconds())

        return data
