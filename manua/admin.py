# manuals_app/admin.py
from django.contrib import admin
from .models import Brand, Product, Manual

class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'created_at')
    search_fields = ('title', 'brand__title')

class ManualAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'pdf', 'created_at')
    search_fields = ('title', 'product__title')
    list_filter = ('product__brand',)

admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manual, ManualAdmin)
