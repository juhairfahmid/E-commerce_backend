from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html , urlencode
from django.db.models import Count
from django.http import HttpRequest
from . import models


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']
    list_per_page = 10

    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode(
                {'collection__id': str(collection.id)}
            )
            )
        return format_html('<a href="{}">{}</a>', url, collection.products_count )
        
    
    def get_queryset(self, request) :
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title','price','inventory_status']
    ordering = ['title']
    search_fields = ['collection']
    list_per_page = 10
    list_filter = ["title"]
        

    def inventory_status(self,product):
        if product.inventory < 10 :
            return "Low"
        else:
            return "OK"

    @admin.action(description="Cleare Inventory")
    def clear_inventory(self, request, queryset: QuerySet):
        update_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{update_count} has successfully updated'
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    list_per_page = 10

admin.site.register(models.Promotion)
    
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)