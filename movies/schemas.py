from ninja import Schema
from typing import List, Optional
from datetime import date, datetime


class GenreIn(Schema):
    """Схема для створення жанру.

    Attributes:
        name: Назва жанру.
    """

    name: str


class GenreOut(Schema):
    """Схема відповіді для жанру.

    Attributes:
        id: Ідентифікатор жанру.
        name: Назва жанру.
    """

    id: int
    name: str


class ReviewIn(Schema):
    """Схема для створення відгуку.

    Attributes:
        text: Текст відгуку.
        score: Оцінка фільму.
    """

    text: str
    score: float


class ReviewOut(Schema):
    """Схема відповіді для відгуку.

    Attributes:
        id: Ідентифікатор відгуку.
        user_id: Ідентифікатор користувача.
        text: Текст відгуку.
        score: Оцінка фільму.
        created_at: Дата створення відгуку.
    """

    id: int
    user_id: int
    text: str
    score: float
    created_at: datetime


class MovieIn(Schema):
    """Схема для створення або оновлення фільму.

    Attributes:
        title: Назва фільму.
        description: Опис фільму.
        release_date: Дата виходу фільму.
        rating: Початковий рейтинг фільму.
        genre_ids: Список ідентифікаторів жанрів.
    """

    title: str
    description: str = ""
    release_date: Optional[date] = None
    rating: float = 0.0
    genre_ids: List[int] = []


class MovieOut(Schema):
    """Схема відповіді для фільму.

    Attributes:
        id: Ідентифікатор фільму.
        title: Назва фільму.
        description: Опис фільму.
        release_date: Дата виходу фільму.
        rating: Середній рейтинг фільму.
        genres: Список жанрів.
        reviews: Список відгуків.
        created_at: Дата створення запису.
    """

    id: int
    title: str
    description: str
    release_date: Optional[date]
    rating: float
    genres: List[GenreOut]
    reviews: List[ReviewOut]
    created_at: datetime