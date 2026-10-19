from django.contrib import admin

from .models import Dish, Order


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "is_featured")
    list_filter = ("category", "is_available", "is_featured")
    search_fields = ("name", "description")
    list_editable = ("price", "is_available", "is_featured")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "dish_name", "quantity", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("dish_name",)
    list_editable = ("status",)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ("dish_name", "unit_price", "created_at")
        return ("dish", "dish_name", "quantity", "unit_price", "created_at")