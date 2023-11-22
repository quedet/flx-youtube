from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from guardian.admin import GuardedModelAdminMixin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(GuardedModelAdminMixin, DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Information", {"fields": ("first_name", "last_name", "birthday", "gender", "profile")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")})
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "first_name", "last_name", "password1", "password2")})
    )

    list_display = ("email", "first_name", "last_name", "is_staff")

    search_fields = ("email", "first_name", "last_name")

    ordering = ("email",)
