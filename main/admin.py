from django.contrib import admin

from .models import *

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selected_date', 'request_time', 'phone_number')
    list_display_list = ('id', 'name', 'selected_date', 'request_time', 'phone_number')
    search_fields = ('id', 'name', 'selected_date', 'request_time', 'phone_number')
    list_filter = ('request_time', 'selected_date')


admin.site.register(Contact, ContactAdmin)