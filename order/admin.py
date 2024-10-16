from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'order_date')

admin.site.register(Order, OrderAdmin)