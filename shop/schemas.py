from ninja import Schema
from decimal import Decimal
from typing import List, Any
from datetime import datetime


class ProductIn(Schema):
    """Схема для створення або оновлення товару.

    Attributes:
        name: Назва товару.
        description: Опис товару.
        price: Ціна товару.
        stock: Кількість товару на складі.
    """

    name: str
    description: str = ""
    price: Decimal
    stock: int = 0


class ProductOut(Schema):
    """Схема відповіді для товару.

    Attributes:
        id: Ідентифікатор товару.
        name: Назва товару.
        description: Опис товару.
        price: Ціна товару.
        stock: Кількість товару на складі.
        created_at: Дата створення запису.
    """

    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    created_at: datetime


class CartItemOut(Schema):
    """Схема відповіді для елемента кошика.

    Attributes:
        id: Ідентифікатор елемента кошика.
        product_id: Ідентифікатор товару.
        product_name: Назва товару.
        quantity: Кількість товару.
    """

    id: int
    product_id: int
    product_name: str
    quantity: int

    @staticmethod
    def resolve_product_name(obj: Any) -> str:
        """Отримує назву товару з пов'язаного об'єкта.

        Args:
            obj: Об'єкт елемента кошика.

        Returns:
            Назва товару.
        """
        return obj.product.name


class AddToCartIn(Schema):
    """Схема для додавання товару до кошика.

    Attributes:
        product_id: Ідентифікатор товару.
        quantity: Кількість товару для додавання.
    """

    product_id: int
    quantity: int = 1


class OrderItemOut(Schema):
    """Схема відповіді для елемента замовлення.

    Attributes:
        id: Ідентифікатор елемента замовлення.
        product_id: Ідентифікатор товару.
        product_name: Назва товару.
        quantity: Кількість товару.
        price: Ціна товару на момент замовлення.
    """

    id: int
    product_id: int
    product_name: str
    quantity: int
    price: Decimal

    @staticmethod
    def resolve_product_name(obj: Any) -> str:
        """Отримує назву товару з пов'язаного об'єкта.

        Args:
            obj: Об'єкт елемента замовлення.

        Returns:
            Назва товару.
        """
        return obj.product.name


class OrderOut(Schema):
    """Схема відповіді для замовлення.

    Attributes:
        id: Ідентифікатор замовлення.
        status: Статус замовлення.
        created_at: Дата створення замовлення.
        items: Список елементів замовлення.
    """

    id: int
    status: str
    created_at: datetime
    items: List[OrderItemOut]


class OrderStatusIn(Schema):
    """Схема для оновлення статусу замовлення.

    Attributes:
        status: Новий статус замовлення.
    """

    status: str