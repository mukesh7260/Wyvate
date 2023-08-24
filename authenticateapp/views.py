from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError 
from django.contrib.auth.models import User
from .models import Cart, Product
from django.conf import settings
import razorpay
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CartItems
from rest_framework.decorators import api_view 



class Register(APIView):
    def post(self, request , format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token':access_token , 'msg':'Register successfully '})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginApi(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        try:
            user = User.objects.get(username=serializer.data.get('username'))
            print(user,'***********')
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        password = user.check_password(serializer.data.get('password'))
        print(password,'&&&&&&&&&&')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        if not password:
            raise ValidationError({'password':'invalid password'})     
        return Response({'message': 'Login successful','access_token':access_token}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def add_to_cart(request):
    serializer = CartitemsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_cart(request,pk):
    cart = CartItems.objects.get(id=pk)
    cart.delete()
    return Response({'delete':'cart_data  has removed successfully '}) 


@api_view(['GET'])
def get_all_items(request):
    items = CartItems.objects.all()
    serializers = CartitemsSerializer(items , many=True ) 
    return Response (serializers.data)


@api_view(['GET'])
def get_specific_items(request,pk):
    items = CartItems.objects.get(id=pk)
    serializers = CartitemsSerializer(items) 
    return Response (serializers.data)




class PaymentView(APIView):
    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = int(serializer.validated_data['amount'] * 100)  # Convert to paise
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': amount, 'currency': 'INR'})
            return Response({'payment_id': payment['id'], 'order_id': payment['order_id']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    