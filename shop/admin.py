from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from shop.models import Product, Category


class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'created_date']
    list_display_links = ['id', 'name']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ShopAdmin)
admin.site.register(Category, MPTTModelAdmin)
