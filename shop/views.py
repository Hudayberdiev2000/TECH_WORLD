from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Shop, Banner, Rule
from .serializers import ShopSerializer, BannerSerializer, RuleSerializer


class ShopDetails(APIView):
    def get(self, request):
        shop = Shop.objects.all().first()
        if shop is None:
            return Response({"message":"There is not any shop yet!"}, status=status.HTTP_200_OK)
        serializers = ShopSerializer(shop)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class BannerList(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RuleList(APIView):
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)