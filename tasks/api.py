from typing import Dict, List, Optional

from django.http import HttpRequest
from ninja import NinjaAPI, Query
from ninja.errors import HttpError

from .models import Task
from .schemas import TaskIn, TaskOut
from .auth import AuthBearer

api = NinjaAPI(auth=AuthBearer())


@api.post("/tasks", response=TaskOut)
def create_task(request: HttpRequest, payload: TaskIn) -> Task:
    """Створює нове завдання.

    Args:
        request: HTTP-запит авторизованого користувача.
        payload: Дані для створення завдання.

    Returns:
        Створений об'єкт завдання.
    """
    task = Task.objects.create(owner=request.user, **payload.dict())
    return task


@api.get("/tasks", response=List[TaskOut])
def list_tasks(
    request: HttpRequest,
    status: Optional[str] = Query(None),
    order_by: str = Query("created_at"),
) -> List[Task]:
    """Повертає список завдань користувача з фільтрацією та сортуванням.

    Args:
        request: HTTP-запит авторизованого користувача.
        status: Фільтр за статусом завдання.
        order_by: Поле для сортування (наприклад, created_at або due_date).

    Returns:
        Список об'єктів завдань.
    """
    qs = Task.objects.filter(owner=request.user)
    if status:
        qs = qs.filter(status=status)
    qs = qs.order_by(order_by)
    return list(qs)


@api.get("/tasks/{task_id}", response=TaskOut)
def get_task(request: HttpRequest, task_id: int) -> Task:
    """Повертає завдання за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        task_id: Ідентифікатор завдання.

    Returns:
        Знайдений об'єкт завдання.

    Raises:
        HttpError: Якщо завдання не знайдено.
    """
    try:
        task = Task.objects.get(id=task_id, owner=request.user)
        return task
    except Task.DoesNotExist:
        raise HttpError(404, "Завдання не знайдено")


@api.put("/tasks/{task_id}", response=TaskOut)
def update_task(request: HttpRequest, task_id: int, payload: TaskIn) -> Task:
    """Оновлює дані завдання.

    Args:
        request: HTTP-запит авторизованого користувача.
        task_id: Ідентифікатор завдання.
        payload: Нові дані завдання.

    Returns:
        Оновлений об'єкт завдання.

    Raises:
        HttpError: Якщо завдання не знайдено.
    """
    try:
        task = Task.objects.get(id=task_id, owner=request.user)
    except Task.DoesNotExist:
        raise HttpError(404, "Завдання не знайдено")
    for attr, value in payload.dict().items():
        setattr(task, attr, value)
    task.save()
    return task


@api.delete("/tasks/{task_id}")
def delete_task(request: HttpRequest, task_id: int) -> Dict[str, bool]:
    """Видаляє завдання за ідентифікатором.

    Args:
        request: HTTP-запит авторизованого користувача.
        task_id: Ідентифікатор завдання.

    Returns:
        Словник зі статусом успішного видалення.

    Raises:
        HttpError: Якщо завдання не знайдено.
    """
    try:
        task = Task.objects.get(id=task_id, owner=request.user)
    except Task.DoesNotExist:
        raise HttpError(404, "Завдання не знайдено")
    task.delete()
    return {"success": True}