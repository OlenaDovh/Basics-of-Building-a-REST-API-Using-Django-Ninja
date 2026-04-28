from ninja import Schema
from typing import Optional
from datetime import date, datetime


class BookIn(Schema):
    """Схема для створення або оновлення книги.

    Attributes:
        title: Назва книги.
        author: Автор книги.
        genre: Жанр книги.
    """

    title: str
    author: str
    genre: str


class BookOut(Schema):
    """Схема відповіді для книги.

    Attributes:
        id: Ідентифікатор книги.
        title: Назва книги.
        author: Автор книги.
        genre: Жанр книги.
        is_available: Чи доступна книга для оренди.
        created_at: Дата створення запису.
    """

    id: int
    title: str
    author: str
    genre: str
    is_available: bool
    created_at: datetime


class RentalIn(Schema):
    """Схема для створення оренди книги.

    Attributes:
        due_date: Дата, до якої потрібно повернути книгу.
    """

    due_date: date


class RentalOut(Schema):
    """Схема відповіді для оренди книги.

    Attributes:
        id: Ідентифікатор оренди.
        book_id: Ідентифікатор книги.
        user_id: Ідентифікатор користувача.
        rented_at: Дата початку оренди.
        due_date: Кінцева дата повернення.
        returned_at: Дата фактичного повернення (може бути відсутня).
    """

    id: int
    book_id: int
    user_id: int
    rented_at: datetime
    due_date: date
    returned_at: Optional[datetime]