from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name_tm = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="category_icons", blank=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = _("Product category")
        verbose_name_plural = _("Product categories")
        
    def __str__(self):
        return self.name_tm
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product_list", on_delete=models.CASCADE)
    name_tm = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product_images", blank=True, null=True)
    desc_tm = models.TextField(_("Description_tm"), blank=True)
    desc_en = models.TextField(_("Description_tm"), blank=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    
    class Meta:
        ordering = ("created_at",)
        db_table = 'products'
        indexes = [
                    models.Index(fields=['price']),
                    models.Index(fields=['-created_at']),
                    ]
        
    def __str__(self):
        return self.name_tm
    
    def sale_price(self):
        # Calculate sale price based on the discount
        price = self.price
        discount = self.discount

        if price is not None and discount is not None:
            sale_price = price - (price * discount / 100)
            return round(sale_price, 2)  # rounding to two decimal places
        else:
            return None
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="product_images", blank=True)
    
    class Meta:
        db_table = 'product_images'
        
    
    
class UserFavourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)