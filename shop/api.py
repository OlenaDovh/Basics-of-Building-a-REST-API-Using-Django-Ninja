from typing import Dict, List

from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.errors import HttpError

from .models import Product, Cart, CartItem, Order, OrderItem
from .schemas import (
    ProductIn, ProductOut,
    CartItemOut, AddToCartIn,
    OrderOut, OrderStatusIn
)
from tasks.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer(), urls_namespace="shop")


@api.post("/products", response=ProductOut)
def create_product(request: HttpRequest, payload: ProductIn) -> Product:
    """Створює новий товар.

    Args:
        request: HTTP-запит авторизованого користувача.
        payload: Дані для створення товару.

    Returns:
        Створений об'єкт товару.
    """
    product = Product.objects.create(**payload.dict())
    return product


@api.get("/products", response=List[ProductOut])
def list_products(request: HttpRequest) -> List[Product]:
    """Повертає список усіх товарів.

    Args:
        request: HTTP-запит авторизованого користувача.

    Returns:
        Список об'єктів товарів.
    """
    return list(Product.objects.all())


@api.get("/products/{product_id}", response=ProductOut)
def get_product(request: HttpRequest, product_id: int) -> Product:
    """Повертає товар за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        product_id: Ідентифікатор товару.

    Returns:
        Знайдений об'єкт товару.

    Raises:
        HttpError: Якщо товар не знайдено.
    """
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise HttpError(404, "Товар не знайдено")


@api.put("/products/{product_id}", response=ProductOut)
def update_product(request: HttpRequest, product_id: int, payload: ProductIn) -> Product:
    """Оновлює дані товару.

    Args:
        request: HTTP-запит авторизованого користувача.
        product_id: Ідентифікатор товару.
        payload: Нові дані товару.

    Returns:
        Оновлений об'єкт товару.

    Raises:
        HttpError: Якщо товар не знайдено.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise HttpError(404, "Товар не знайдено")
    for attr, value in payload.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@api.delete("/products/{product_id}")
def delete_product(request: HttpRequest, product_id: int) -> Dict[str, bool]:
    """Видаляє товар за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        product_id: Ідентифікатор товару.

    Returns:
        Словник зі статусом успішного видалення.

    Raises:
        HttpError: Якщо товар не знайдено.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise HttpError(404, "Товар не знайдено")
    product.delete()
    return {"success": True}


def get_or_create_cart(user: User) -> Cart:
    """Повертає існуючий кошик користувача або створює новий.

    Args:
        user: Користувач, для якого потрібно отримати або створити кошик.

    Returns:
        Об'єкт кошика користувача.
    """
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api.get("/cart", response=List[CartItemOut])
def get_cart(request: HttpRequest) -> List[CartItem]:
    """Повертає вміст кошика авторизованого користувача.

    Args:
        request: HTTP-запит авторизованого користувача.

    Returns:
        Список об'єктів товарів у кошику.
    """
    cart = get_or_create_cart(request.user)
    return list(cart.items.select_related('product').all())


@api.post("/cart", response=CartItemOut)
def add_to_cart(request: HttpRequest, payload: AddToCartIn) -> CartItem:
    """Додає товар до кошика користувача.

    Args:
        request: HTTP-запит авторизованого користувача.
        payload: Дані товару та кількості для додавання в кошик.

    Returns:
        Об'єкт товару в кошику.

    Raises:
        HttpError: Якщо товар не знайдено.
    """
    try:
        product = Product.objects.get(id=payload.product_id)
    except Product.DoesNotExist:
        raise HttpError(404, "Товар не знайдено")

    cart = get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += payload.quantity
    else:
        item.quantity = payload.quantity
    item.save()
    return item


@api.delete("/cart/{item_id}")
def remove_from_cart(request: HttpRequest, item_id: int) -> Dict[str, bool]:
    """Видаляє товар із кошика користувача.

    Args:
        request: HTTP-запит авторизованого користувача.
        item_id: Ідентифікатор товару в кошику.

    Returns:
        Словник зі статусом успішного видалення.

    Raises:
        HttpError: Якщо товар у кошику не знайдено.
    """
    cart = get_or_create_cart(request.user)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        raise HttpError(404, "Товар у кошику не знайдено")
    item.delete()
    return {"success": True}


@api.post("/orders", response=OrderOut)
def create_order(request: HttpRequest) -> Order:
    """Створює замовлення на основі поточного кошика користувача.

    Args:
        request: HTTP-запит авторизованого користувача.

    Returns:
        Створений об'єкт замовлення.

    Raises:
        HttpError: Якщо кошик порожній.
    """
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product').all()

    if not items:
        raise HttpError(400, "Кошик порожній")

    order = Order.objects.create(user=request.user)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart.items.all().delete()  # очищаємо кошик після замовлення
    return order


@api.get("/orders", response=List[OrderOut])
def list_orders(request: HttpRequest) -> List[Order]:
    """Повертає список замовлень авторизованого користувача.

    Args:
        request: HTTP-запит авторизованого користувача.

    Returns:
        Список об'єктів замовлень користувача.
    """
    return list(Order.objects.filter(user=request.user).prefetch_related('items__product'))


@api.get("/orders/{order_id}", response=OrderOut)
def get_order(request: HttpRequest, order_id: int) -> Order:
    """Повертає замовлення за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        order_id: Ідентифікатор замовлення.

    Returns:
        Знайдений об'єкт замовлення.

    Raises:
        HttpError: Якщо замовлення не знайдено.
    """
    try:
        return Order.objects.prefetch_related('items__product').get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        raise HttpError(404, "Замовлення не знайдено")


@api.patch("/orders/{order_id}/status", response=OrderOut)
def update_order_status(
        request: HttpRequest,
        order_id: int,
        payload: OrderStatusIn,
) -> Order:
    """Оновлює статус замовлення.

    Args:
        request: HTTP-запит авторизованого користувача.
        order_id: Ідентифікатор замовлення.
        payload: Дані з новим статусом замовлення.

    Returns:
        Оновлений об'єкт замовлення.

    Raises:
        HttpError: Якщо статус недопустимий або замовлення не знайдено.
    """
    valid_statuses = ['pending', 'shipped', 'delivered']
    if payload.status not in valid_statuses:
        raise HttpError(400, f"Невірний статус. Доступні: {valid_statuses}")
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        raise HttpError(404, "Замовлення не знайдено")
    order.status = payload.status
    order.save()
    return order
