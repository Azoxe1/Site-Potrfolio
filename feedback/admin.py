from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selected_date', 'request_time', 'phone_number')
    list_display_list = ('id', 'name', 'selected_date', 'request_time', 'phone_number')
    search_fields = ('id', 'name', 'selected_date', 'request_time', 'phone_number')
    list_filter = ('request_time', 'selected_date')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_list = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'email')
    list_filter = ('id', 'username', 'email')


admin.site.register(Contact, ContactAdmin)