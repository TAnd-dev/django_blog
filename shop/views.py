from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from shop.forms import ChangeBasketForm
from shop.models import Product, Category, Basket, Purchase


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
        context['basket_products'] = Basket.objects.values_list('product__slug', flat=True).filter(
            user=self.request.user)
        return context


class BasketView(LoginRequiredMixin, CreateView):
    model = Purchase
    fields = ('email', 'tel', 'country', 'city', 'street')
    template_name = 'shop/basket.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        tel = form.cleaned_data['tel']
        country = form.cleaned_data['country']
        city = form.cleaned_data['city']
        street = form.cleaned_data['street']
        user = self.request.user
        products = Basket.objects.values_list('product', flat=True).filter(user=self.request.user)
        total_price = Basket.objects.filter(user=self.request.user).aggregate(
            total_price=Sum(F('product__price') * F('quantity')))
        purchase = Purchase.objects.create(user=user, total_price=total_price.get('total_price'), email=email, tel=tel,
                                           country=country,
                                           city=city, street=street)
        purchase.products.add(*products)
        Basket.objects.filter(user=self.request.user).delete()
        return redirect('history_purchases')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = Basket.objects.filter(user=self.request.user).aggregate(
            total_price=Sum(F('product__price') * F('quantity')))
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        context['total_price'] = total_price.get('total_price')
        return context


def change_basket(request, pk):
    basket = Basket.objects.get(pk=pk)

    if request.method == 'POST':
        form = ChangeBasketForm(request.POST, instance=basket)
        if form.is_valid():
            form.save()
            return redirect('basket')
    else:
        form = ChangeBasketForm(instance=basket)

    return render(request, 'shop/change_basket.html', {'form': form, 'product': basket.product.name})


@login_required
def add_to_basket(request, slug):
    product = Product.objects.get(slug=slug)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        Basket.objects.get(user=request.user, product=product).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def buy_product(request, slug):
    product = Product.objects.get(slug=slug)
    baskets = Basket.objects.filter(user=request.user, product=product)
    print(product, baskets)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

    return redirect('basket')


@login_required
def basket_delete(request, pk):
    product = Basket.objects.get(id=pk)
    product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class HistoryPurchases(ListView):
    model = Purchase
    template_name = 'shop/history_purchases.html'
    context_object_name = 'purchases'
    paginate = 10
    allow_empty = True
