from django import forms

from shop.models import Basket


class ChangeBasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['quantity']
        widgets = {'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'inputQuantity'})}
