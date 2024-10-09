from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'payment_type',
            'product_price',
            'delivery_fee',
            'discount',
            'total_amount',
            'address',
            'order_date',
            'user',
        ]
        read_only_fields = ['id', 'order_date']