from django.contrib import admin

from web.product.models import Product, Order, DeliveryService, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id", "get_user", "get_product",
        "get_delivery", "products_count", "invoice"
    ]

    raw_id_fields = ('user', 'product', 'delivery')

    def get_user(self, order):
        return order.user.email

    get_user.admin_order_field = "email"
    get_user.short_description = "user email"

    def get_delivery(self, order):
        return order.delivery.title

    get_delivery.admin_order_field = "delivery"
    get_delivery.short_description = "delivery method"

    def get_product(self, order):
        return order.product.title

    get_product.admin_order_field = "product"
    get_product.short_description = "product name"


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DeliveryService, DeliveryServiceAdmin)
