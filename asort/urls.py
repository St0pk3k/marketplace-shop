from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('clear-history/', views.clear_order_history, name='clear_order_history'),
    path('about/', views.about, name='about'),
    path('checkout/', views.checkout, name='checkout'),
    path('bank/', views.bank_payment, name='bank'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]