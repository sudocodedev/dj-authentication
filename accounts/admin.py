from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount


class UserAccountAdmin(UserAdmin):
    list_display = ("email", "username", "date_joined", "last_login", "is_superuser", "is_staff", "is_active",)
    list_filter = ("email","username", "is_staff", "is_active",)
    search_fields = ("email", "username",)
    read_only = ("last_login", "date_joined",)
    ordering = ("email",)
    fieldsets = (
        (None, {'fields': ('avatar', 'email', 'username', 'password', 'login_sms_otp', 'phonenumber')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phonenumber', 'avatar', 'password1', 'password2','is_staff', 'is_active', 'is_superuser')
        }),
    )

admin.site.register(UserAccount, UserAccountAdmin)

