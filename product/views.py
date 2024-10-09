from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Category, Product, UserFavourites
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, UserFavouritesSerializer





class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryProducts(APIView):
    def get(self, request):
        
        limit = request.GET.get('limit', 10)
        sortBy = request.GET.get('sortBy')
        if not (sortBy == 'created_at' or sortBy == 'price'):
            sortBy = 'created_at'
            
        try:
            limit = int(limit)
        except:
            return Response({'error': 'limit must be an integer'}, status=status.HTTP_404_NOT_FOUND)
        if limit <= 0:
            limit = 10
        order = request.GET.get('order')
        
        category_id = request.GET.get('category_id')
        queryset = Product.objects.filter(category=category_id)
        
        ordering = f"-{sortBy}" if order == 'desc' else sortBy
        products = queryset.order_by(ordering)[:limit]
            
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductList(APIView):
    def get(self, request):
        sortBy = request.GET.get('sortBy')
        
        if not (sortBy == 'created_at' or sortBy == 'price'):
            sortBy = 'created_at'
            
        order = request.GET.get('order')
        limit = request.GET.get('limit', 10)
    
        try:
            limit = int(limit)
        except:
            return Response({'error': 'limit must be an integer'}, status=status.HTTP_404_NOT_FOUND)
        
        if limit <= 0:
            limit = 10
            
        ordering = f"-{sortBy}" if order == 'desc' else sortBy
        products = Product.objects.order_by(ordering)[:limit]
            
        serializer = ProductSerializer(products, many=True)
        
        if products:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class ProductSearchView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        
        search = data['search']
        
        if len(search) == 0:
            search_results = Product.objects.order_by('-created_at').all()
        else:
            search_results = Product.objects.filter(
                Q(desc_tm__icontains=search) | Q(name_tm__icontains=search)
            )
            
        search_results = ProductSerializer(search_results, many=True)
        
        return Response(
            {'search_results': search_results.data},
            status=status.HTTP_200_OK
        )
        

class ProductDetails(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        data = serializer.data
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True)
        data['images'] = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    
    
class UserFavouritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user_favourites = UserFavourites.objects.filter(user=request.user)
        serializer = UserFavouritesSerializer(user_favourites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        product_id = request.query_params.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if UserFavourites.objects.filter(product=product, user=user).exists():
            return Response({'error': 'This product is already in your favourites.'}, status=status.HTTP_400_BAD_REQUEST)
            
        UserFavourites.objects.create(user=user, product=product)
        favorite_products = UserFavourites.objects.filter(user=user)
        serializer = UserFavouritesSerializer(favorite_products, many=True)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        product_id = request.query_params.get('product_id')
        product = Product.objects.get(id=product_id)
        try:
            favourite = UserFavourites.objects.get(product=product, user=request.user)
        except UserFavourites.DoesNotExist:
            return Response({'error': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)
                    
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)