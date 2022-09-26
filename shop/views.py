from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from shop.models import Product, Category, Basket


class Shop(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    allow_empty = True


class ShopCategory(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_categories'] = Category.objects.filter(slug=self.kwargs['slug']).first().get_ancestors(
            include_self=True)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_categories'] = Category.objects.filter(product__slug=self.kwargs['slug'])
        context['basket_products'] = Basket.objects.get(user=self.request.user).products.all()
        return context


def add_to_basket(request, slug):
    product = Product.objects.get(slug=slug)
    basket = Basket.objects.get(user=request.user)
    if product in basket.products.all():
        basket.products.remove(product)
        basket.quantity -= 1
    else:
        basket.products.add(product)
        basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
