from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Модель товару.

    Attributes:
        name: Назва товару.
        description: Опис товару.
        price: Ціна товару.
        stock: Кількість товару на складі.
        created_at: Дата створення запису.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає назву товару.

        Returns:
            Назва товару.
        """
        return self.name


class Cart(models.Model):
    """Модель кошика користувача.

    Attributes:
        user: Користувач, якому належить кошик.
        created_at: Дата створення кошика.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення кошика.

        Returns:
            Рядок у форматі "Кошик <username>".
        """
        return f"Кошик {self.user.username}"


class CartItem(models.Model):
    """Модель елемента кошика.

    Attributes:
        cart: Кошик, до якого належить елемент.
        product: Товар у кошику.
        quantity: Кількість товару.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """Повертає рядкове представлення елемента кошика.

        Returns:
            Рядок у форматі "<назва товару> x<кількість>".
        """
        return f"{self.product.name} x{self.quantity}"


class Order(models.Model):
    """Модель замовлення.

    Attributes:
        user: Користувач, який створив замовлення.
        status: Статус замовлення.
        created_at: Дата створення замовлення.
    """

    STATUS_CHOICES = [
        ('pending', 'У процесі'),
        ('shipped', 'Відправлений'),
        ('delivered', 'Доставлений'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення замовлення.

        Returns:
            Рядок у форматі "Замовлення #id - username".
        """
        return f"Замовлення #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """Модель елемента замовлення.

    Attributes:
        order: Замовлення, до якого належить елемент.
        product: Товар у замовленні.
        quantity: Кількість товару.
        price: Ціна товару на момент замовлення.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        """Повертає рядкове представлення елемента замовлення.

        Returns:
            Рядок у форматі "<назва товару> x<кількість>".
        """
        return f"{self.product.name} x{self.quantity}"