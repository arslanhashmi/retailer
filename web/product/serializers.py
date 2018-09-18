from rest_framework import serializers

from web.account.serializers import UserSerializer
from web.product.models import Product, Order, Category, DeliveryService, WishList


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'title'
        )


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'image', 'price', 'categories',
        )

    # noinspection PyMethodMayBeStatic
    def get_price(self, product):
        return dict(amount=product.price.amount, currency=product.price.currency.name)


class DeliveryServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryService
        fields = ('id', 'title', 'price')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    delivery = DeliveryServiceSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'product', 'delivery', 'products_count', 'invoice',
        )
