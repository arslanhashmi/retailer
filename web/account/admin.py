from django.contrib import admin

from web.account.models import User


class UserAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search users
    """
    list_display = [
        'email',
        'is_active',
        'is_superuser',
    ]

    search_fields = ['email']


admin.site.register(User, UserAdmin)
