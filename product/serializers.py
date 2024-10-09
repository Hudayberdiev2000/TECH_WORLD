from rest_framework import serializers
from .models import Product, Category, ProductImage, UserFavourites

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name_tm = serializers.CharField(max_length=255)
    name_en = serializers.CharField(max_length=255)
    icon = serializers.ImageField(allow_empty_file=True, required=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_tm = validated_data.get('name_tm', instance.name_tm)
        instance.name_en = validated_data.get('name_en', instance.name_en)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name_tm = serializers.CharField(max_length=255)
    name_en = serializers.CharField(max_length=255)
    desc_tm = serializers.CharField(max_length=1000)
    desc_en = serializers.CharField(max_length=1000)
    price = serializers.IntegerField()
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    category = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    discount = serializers.IntegerField()
    sale_price = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_sale_price(self, obj):
        # Calculate sale price based on the discount
        price = obj.price
        discount = obj.discount

        if price is not None and discount is not None:
            sale_price = price - (price * discount / 100)
            return round(sale_price, 2)  # rounding to two decimal places
        else:
            return None
        
    def get_category(self, obj):
        return obj.category.name_tm

    
class ProductImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), allow_null=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, required=False)

    def create(self, validated_data):
        return ProductImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    
class UserFavouritesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductSerializer()
    
    