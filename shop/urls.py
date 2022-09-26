from django.urls import path

from shop.views import Shop, ProductDetail, ShopCategory

urlpatterns = [
    path('', Shop.as_view(), name='shop'),
    path('category/<str:slug>/', ShopCategory.as_view(), name='product_category'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail')
]