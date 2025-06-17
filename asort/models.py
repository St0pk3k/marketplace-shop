from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    REQUIRED_FIELDS = ['full_name', 'address', 'phone']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    size = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Размер",
        help_text="Введите размер свободно, например: 46, 47, XL, M и т.д."
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('courier', 'Курьером'),
        ('pickup', 'Самовывоз'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        blank=False,
        default='pickup'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ от {self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} — {self.quantity} шт."