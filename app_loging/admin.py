from django.contrib import admin

from app_loging.models import User, ConfirmEmailToken


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_list = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'email')
    list_filter = ('id', 'username', 'email')


class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'key')
    list_display_list = ('user', 'created_at', 'key')


admin.site.register(User, UserAdmin)
admin.site.register(ConfirmEmailToken, ConfirmEmailTokenAdmin)
