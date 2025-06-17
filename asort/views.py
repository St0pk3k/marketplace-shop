from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from .models import Product, Category, Order, OrderItem
from .forms import CustomUserCreationForm, UserUpdateForm, OrderForm


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.annotate(name_lower=Lower('name')).filter(name_lower__contains=query.lower())

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sizes = Product.objects.values_list('size', flat=True).distinct().exclude(size__isnull=True).exclude(size__exact='')

    size_filter = request.GET.get('size', 'all')
    if size_filter and size_filter != 'all':
        products = products.filter(size=size_filter)

    context = {
        'products': products,
        'categories': categories,
        'sizes': sizes,
        'selected_size': size_filter,
    }
    return render(request, 'asort/product_list.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'asort/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'user_form': form,
        'orders': orders,
    }
    return render(request, 'asort/profile.html', context)


@login_required
def clear_order_history(request):
    Order.objects.filter(user=request.user).delete()
    return redirect('profile')


def about(request):
    return render(request, 'asort/about.html')


def cart(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total_price = Decimal('0')
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'asort/cart.html', context)


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
        request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart and cart[str(product_id)] > 1:
        cart[str(product_id)] -= 1
        request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total_price = Decimal('0')
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated and not request.user.is_superuser:
                order.user = request.user
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )
            request.session['order_total_price'] = str(total_price)
            request.session['cart'] = {}
            return redirect('bank')
    else:
        form = OrderForm()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }
    return render(request, 'asort/checkout.html', context)


def bank_payment(request):
    total_price_str = request.session.get('order_total_price', '0')
    total_price = Decimal(total_price_str)

    if request.method == 'POST':
        request.session.pop('order_total_price', None)
        return redirect('thank_you')

    return render(request, 'asort/bank.html', {'total_price': total_price})


def thank_you(request):
    return render(request, 'asort/thank_you.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'asort/product_detail.html', {'product': product})