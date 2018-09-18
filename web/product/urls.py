from django.urls import path
from rest_framework import routers

from web.product.views import ProductListView, PlaceOrderView, WishListView

app_name = 'product'

router = routers.DefaultRouter()
router.register(r'products', ProductListView)
router.register(r'place/order', PlaceOrderView)

urlpatterns = [
    path(r'wishlist/add/<int:product_id>/', WishListView.as_view()),
    path(r'wishlist/', WishListView.as_view()),
]

urlpatterns.extend(router.urls)