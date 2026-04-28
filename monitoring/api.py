from typing import Dict, List

from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.errors import HttpError

from .models import Server, Metric, Alert
from .schemas import ServerIn, ServerOut, ServerStatusIn, MetricIn, MetricOut, AlertOut
from tasks.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer(), urls_namespace="monitoring")

CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 80.0
LOAD_THRESHOLD = 80.0


@api.post("/servers", response=ServerOut)
def create_server(request: HttpRequest, payload: ServerIn) -> Server:
    """Створює новий сервер для авторизованого користувача.

    Args:
        request: HTTP-запит авторизованого користувача.
        payload: Дані для створення сервера.

    Returns:
        Створений об'єкт сервера.

    Raises:
        HttpError: Якщо статус сервера має недопустиме значення.
    """
    if payload.status not in ['online', 'offline']:
        raise HttpError(400, "Статус може бути тільки 'online' або 'offline'")
    server = Server.objects.create(owner=request.user, **payload.dict())
    return server


@api.get("/servers", response=List[ServerOut])
def list_servers(request: HttpRequest) -> List[Server]:
    """Повертає список серверів авторизованого користувача.

    Args:
        request: HTTP-запит авторизованого користувача.

    Returns:
        Список об'єктів серверів.
    """
    return list(Server.objects.filter(owner=request.user))


@api.get("/servers/{server_id}", response=ServerOut)
def get_server(request: HttpRequest, server_id: int) -> Server:
    """Повертає сервер за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.

    Returns:
        Знайдений об'єкт сервера.

    Raises:
        HttpError: Якщо сервер не знайдено.
    """
    try:
        return Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")


@api.put("/servers/{server_id}", response=ServerOut)
def update_server(request: HttpRequest, server_id: int, payload: ServerIn) -> Server:
    """Оновлює дані сервера.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.
        payload: Нові дані сервера.

    Returns:
        Оновлений об'єкт сервера.

    Raises:
        HttpError: Якщо сервер не знайдено.
    """
    try:
        server = Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")
    for attr, value in payload.dict().items():
        setattr(server, attr, value)
    server.save()
    return server


@api.delete("/servers/{server_id}")
def delete_server(request: HttpRequest, server_id: int) -> Dict[str, bool]:
    """Видаляє сервер за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.

    Returns:
        Словник зі статусом успішного видалення.

    Raises:
        HttpError: Якщо сервер не знайдено.
    """
    try:
        server = Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")
    server.delete()
    return {"success": True}


@api.patch("/servers/{server_id}/status", response=ServerOut)
def update_server_status(
    request: HttpRequest,
    server_id: int,
    payload: ServerStatusIn,
) -> Server:
    """Оновлює статус сервера.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.
        payload: Дані з новим статусом сервера.

    Returns:
        Оновлений об'єкт сервера.

    Raises:
        HttpError: Якщо статус недопустимий або сервер не знайдено.
    """
    if payload.status not in ['online', 'offline']:
        raise HttpError(400, "Статус може бути тільки 'online' або 'offline'")
    try:
        server = Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")
    server.status = payload.status
    server.save()
    return server


@api.post("/servers/{server_id}/metrics", response=MetricOut)
def add_metric(request: HttpRequest, server_id: int, payload: MetricIn) -> Metric:
    """Додає метрики для сервера та створює попередження за перевищення порогів.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.
        payload: Дані метрик сервера.

    Returns:
        Створений об'єкт метрики.

    Raises:
        HttpError: Якщо сервер не знайдено.
    """
    try:
        server = Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")

    metric = Metric.objects.create(server=server, **payload.dict())

    alerts = []
    if payload.cpu > CPU_THRESHOLD:
        alerts.append(f"CPU критичний: {payload.cpu}%")
    if payload.memory > MEMORY_THRESHOLD:
        alerts.append(f"Пам'ять критична: {payload.memory}%")
    if payload.load > LOAD_THRESHOLD:
        alerts.append(f"Навантаження критичне: {payload.load}%")

    for message in alerts:
        Alert.objects.create(server=server, message=message)

    return metric


@api.get("/servers/{server_id}/metrics", response=List[MetricOut])
def list_metrics(request: HttpRequest, server_id: int) -> List[Metric]:
    """Повертає список метрик сервера.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.

    Returns:
        Список об'єктів метрик.

    Raises:
        HttpError: Якщо сервер не знайдено.
    """
    try:
        server = Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")
    return list(server.metrics.all())


@api.get("/servers/{server_id}/alerts", response=List[AlertOut])
def list_alerts(request: HttpRequest, server_id: int) -> List[Alert]:
    """Повертає список попереджень сервера.

    Args:
        request: HTTP-запит авторизованого користувача.
        server_id: Ідентифікатор сервера.

    Returns:
        Список об'єктів попереджень.

    Raises:
        HttpError: Якщо сервер не знайдено.
    """
    try:
        server = Server.objects.get(id=server_id, owner=request.user)
    except Server.DoesNotExist:
        raise HttpError(404, "Сервер не знайдено")
    return list(server.alerts.all())