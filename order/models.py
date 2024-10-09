from django.db import models
from product.models import Product
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    TERMINAL = 'terminal'
    CASH = 'cash'

    PAYMENT_CHOICES = [(TERMINAL, 'Terminal'), (CASH, 'Cash'),]

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=CASH)
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    delivery_fee = models.IntegerField()
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.full_name}'s order."