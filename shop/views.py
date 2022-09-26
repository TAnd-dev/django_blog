from django.shortcuts import render
from django.views.generic import ListView, DetailView

from shop.models import Product, Category


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
        return context
