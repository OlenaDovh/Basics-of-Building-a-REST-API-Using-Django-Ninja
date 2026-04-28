from ninja import Schema
from datetime import date, datetime
from typing import Optional


class TaskIn(Schema):
    """Схема для створення або оновлення завдання.

    Attributes:
        title: Назва завдання.
        description: Опис завдання.
        status: Статус завдання (pending або done).
        due_date: Дата дедлайну виконання.
    """

    title: str
    description: str = ""
    status: str = "pending"
    due_date: Optional[date] = None


class TaskOut(Schema):
    """Схема відповіді для завдання.

    Attributes:
        id: Ідентифікатор завдання.
        title: Назва завдання.
        description: Опис завдання.
        status: Статус завдання.
        due_date: Дата дедлайну виконання.
        created_at: Дата створення завдання.
        owner_id: Ідентифікатор власника завдання.
    """

    id: int
    title: str
    description: str
    status: str
    due_date: Optional[date]
    created_at: datetime
    owner_id: int