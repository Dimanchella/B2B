from django.contrib import admin

from .models import Orders, OrdersDetail, ExchangeNode


class OrdersDetailInLine(admin.TabularInline):
    model = OrdersDetail


class OrdersAdmin(admin.ModelAdmin):
    search_fields = ['number', 'date', 'user__username', 'user__email']

    inlines = [
        OrdersDetailInLine
    ]


admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrdersDetail)
admin.site.register(ExchangeNode)
