from django.contrib import admin

from .models import Product, Store, StoreItem, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


class StoreItemInline(admin.TabularInline):
    model = StoreItem
    extra = 0


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_location_name')
    inlines = (StoreItemInline,)

    def get_location_name(self, obj):
        return obj.location.city.name, obj.location.address
    get_location_name.short_description = 'Location' #Renames column head
    get_location_name.admin_order_field = 'location__city' #Allows column order sorting

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_city_name')
    inlines = (OrderItemInline,)

    def get_city_name(self, obj):
        return obj.city.name
    get_city_name.short_description = 'City' #Renames column head
    get_city_name.admin_order_field = 'city' #Allows column order sorting


admin.site.register(Product, ProductAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Order, OrderAdmin)
