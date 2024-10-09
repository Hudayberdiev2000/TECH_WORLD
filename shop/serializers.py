from rest_framework import serializers


class ShopSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title_tm = serializers.CharField(max_length=150)
    title_en = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    address_tm = serializers.CharField(max_length=300)
    address_en = serializers.CharField(max_length=300)
    

class BannerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image_url = serializers.ImageField(allow_null=True, required=False)
    

class RuleSerializer(serializers.Serializer):
    description_tm = serializers.CharField()
    description_en = serializers.CharField()
