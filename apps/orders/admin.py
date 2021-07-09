from django.contrib import admin

from apps.orders.models import OrderPizza


@admin.register(OrderPizza)
class OrderPizzaAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "pizza", "price", "is_paid", "is_enable")
    list_select_related = ('user', 'pizza')
    search_fields = ('user__username', 'pizza__name')
    autocomplete_fields = ('user', 'pizza')
    list_filter = ('is_enable', 'is_paid')
