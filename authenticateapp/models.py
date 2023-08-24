from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def add_to_cart(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove_from_cart(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1,null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

  