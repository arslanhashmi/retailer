from rest_framework import views, viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from web.product.models import Product, Order, DeliveryService, WishList
from web.product.serializers import ProductSerializer, OrderSerializer


class ProductListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        products = Product.objects.all()

        product_kw = self.request.query_params.get('product')
        if product_kw:
            products = products.filter(title__icontains=product_kw)

        category_kw = self.request.query_params.get('category')
        if category_kw:
            products = products.filter(categories__title__icontains=category_kw)

        return products


class PlaceOrderView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = Product.get_or_none(pk=self.request.data.get('product_id'))
        if not product:
            raise ValidationError("Invalid product ID")

        delivery = DeliveryService.get_or_none(pk=self.request.data.get('delivery_id'))
        if not delivery:
            raise ValidationError("Invalid delivery ID")

        serializer.save(user=self.request.user, product=product, delivery=delivery)


class WishListView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wished_products = ProductSerializer([
            wish_list_item.product
            for wish_list_item in WishList.objects.filter(user=request.user)
        ], many=True).data

        return Response(data=wished_products, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        product = Product.get_or_none(pk=product_id)
        if product:
            __, created = WishList.objects.get_or_create(user=request.user, product=product)

            if created:
                response = Response(
                    data=dict(success=f'{product.title} has been added into your Wishlist.'),
                    status=status.HTTP_200_OK
                )
            else:
                response = Response(
                    data=dict(warning=f'{product.title} is already in your Wishlist.'),
                    status=status.HTTP_200_OK
                )
        else:
            response = Response(
                data=dict(error=f'Invalid product ID "{product_id}".'),
                status=status.HTTP_400_BAD_REQUEST
            )

        return response
