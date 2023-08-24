from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cart, Product, CartItem , CartItems
from django.contrib.auth.models import Group


class RegisterSerializer(serializers.ModelSerializer):
    GROUP_CHOICE = [
        ("Admin", "Admin"),
        ("User", "User"),
        ("Vender", "Vender"),
    ]
    group = serializers.ChoiceField(choices=GROUP_CHOICE)
        
    
    class Meta:
        model = User
        fields = ['id','username','email','password', "group"] 
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group = validated_data.pop("group",None)
        groups, created = Group.objects.get_or_create(name=group)
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        groups.user_set.add(user)
        return user
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products']

class CartitemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItems
        fields = ['user','product_name','quantity','price']


class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)