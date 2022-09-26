from django.urls import path

from shop.views import Shop, ProductDetail, ShopCategory, add_to_basket

urlpatterns = [
    path('', Shop.as_view(), name='shop'),
    path('category/<str:slug>/', ShopCategory.as_view(), name='product_category'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<str:slug>/add_to_basket/', add_to_basket, name='add_to_basket'),
]