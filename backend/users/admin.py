from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "full_name", "contractor")

    fieldsets = UserAdmin.fieldsets + (
        ("Реквизиты 1С", {"fields": ("full_name", "contractor")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Реквизиты 1С", {"fields": ("full_name", "contractor")}),
    )

    search_fields = ("full_name", "username", "contractor")
    ordering = ("full_name", "username", "contractor")


admin.site.register(CustomUser, CustomUserAdmin)
