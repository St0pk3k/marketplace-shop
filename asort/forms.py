from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, label='Имя')
    address = forms.CharField(max_length=200, label='Адрес')
    phone = forms.CharField(max_length=20, label='Телефон')

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'full_name', 'address', 'phone']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'address', 'phone']
        labels = {
            'full_name': 'Имя',
            'address': 'Адрес',
            'phone': 'Телефон',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'phone', 'delivery_method']
        labels = {
            'name': 'Ваше имя',
            'address': 'Адрес доставки',
            'phone': 'Телефон',
            'delivery_method': 'Способ доставки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_method'].required = True
