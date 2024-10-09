from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, Adddress
from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer, AddressSerializer
from cart.models import Cart


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                full_name=serializer.validated_data['full_name'],
                phone_number=serializer.validated_data['phone_number'],
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            shopping_cart = Cart.objects.create(user=user)
            shopping_cart.save()
            
            return Response({
                'message': 'User registered successfully!',
                "access_token": access_token,
                "refresh_token": str(refresh)
                }, status=status.HTTP_201_CREATED, headers={'Authorization': f'Bearer {access_token}'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            user = User.objects.filter(phone_number=phone_number).first()

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
            
        if not refresh_token:
            return Response({'message': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token) 
            token.blacklist()
            return Response("Logged out successfully!", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class AddressListCreateView(APIView):
    def get(self, request):
       if not request.user.is_authenticated():
           return Response({"message": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
       user = request.user
       addresses = Adddress.objects.filter(user=user)
       serializer = AddressSerializer(addresses, many=True)
       
       return Response(serializer.data, status=status.HTTP_200_OK)
   
    def post(self, request):
        if not request.user.is_authenticated():
           return Response({"message": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
       
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddressDetailView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated():
           return Response({"message": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        address = Adddress.objects.get(pk=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        if not request.user.is_authenticated():
           return Response({"message": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        address = Adddress.objects.get(pk=pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not request.user.is_authenticated():
           return Response({"message": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        address = Adddress.objects.get(pk=pk)
        address.delete()
        return Response({"message": "Address deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
       
       
class UserdetailView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)