from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer
from cart.models import Cart, CartItem


class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        
        serializer = OrderSerializer(orders, many=True)

        if not orders.exists():
            return Response({'message':'You have no orders'}, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = self.request.user.id        
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            
            cart_items.delete()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class OderpreviewView(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = self.request.user
        
        cart = Cart.objects.get(user=user) 
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return Response({'message':'you dont have any product in your cart'}, status=status.HTTP_200_OK)
        
        product_price = 0.0
        delivery_fee = 15
        discount = 0.0
        total_amount = 0.0
        for cart_item in cart_items:
            for _ in range(cart_item.count):
                product_price = cart_item.product.price/1
        if product_price > 800:
            discount = 20.0
        elif product_price > 500:
            discount = 10.0
        
        total_amount = product_price + delivery_fee - (product_price * discount / 100)
        
        result = {}
        result['product_price'] = product_price
        result['delivery_fee'] = delivery_fee
        result['discount'] = discount
        result['total_amount'] = total_amount
        
        return Response(result, status=status.HTTP_200_OK)
        
        
