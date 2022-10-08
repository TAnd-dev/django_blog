from django.urls import path

from shop.views import Shop, ProductDetail, ShopCategory, BasketView, change_basket, add_to_basket, basket_delete, \
    buy_product, HistoryPurchases

urlpatterns = [
    path('', Shop.as_view(), name='shop'),
    path('basket', BasketView.as_view(), name='basket'),
    path('buy_product/<str:slug>', buy_product, name='buy_product'),
    path('history_purchases', HistoryPurchases.as_view(), name='history_purchases'),
    path('change_basket/<int:pk>/', change_basket, name='change_basket'),
    path('basket_delete/<int:pk>/', basket_delete, name='basket_delete'),
    path('category/<str:slug>/', ShopCategory.as_view(), name='product_category'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<str:slug>/add_to_basket/', add_to_basket, name='add_to_basket'),
]
