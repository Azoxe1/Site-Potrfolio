from django.contrib import admin

from .models import *


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'products_image', 'description',
                    'price', 'feachured', 'product_status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product',
                    'review', 'rating']


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description',
                    'stack', 'git', 'project_image']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'city',
                    'street', 'house', 'structure', 'building', 'apartment'
        , 'phone']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'dt',
                    'state', 'contact']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name',
                    'quantity']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(ProductReview, ProductReviewAdmin)

admin.site.register(Projects, ProjectsAdmin)
