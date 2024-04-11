from django.contrib import admin

from .models import Order, OrderDetail, ExchangeNode


class OrderDetailInLine(admin.TabularInline):
    model = OrderDetail


class OrdersAdmin(admin.ModelAdmin):
    search_fields = ['number', 'date', 'user__username', 'user__email']

    inlines = [
        OrderDetailInLine
    ]


admin.site.register(Order, OrdersAdmin)
admin.site.register(OrderDetail)
admin.site.register(ExchangeNode)

