from ninja import Schema
from typing import List
from datetime import datetime


class TagIn(Schema):
    """Схема для створення тегу.

    Attributes:
        name: Назва тегу.
    """

    name: str


class TagOut(Schema):
    """Схема для відображення тегу.

    Attributes:
        id: Ідентифікатор тегу.
        name: Назва тегу.
    """

    id: int
    name: str


class CommentIn(Schema):
    """Схема для створення коментаря.

    Attributes:
        text: Текст коментаря.
    """

    text: str


class CommentOut(Schema):
    """Схема для відображення коментаря.

    Attributes:
        id: Ідентифікатор коментаря.
        author_id: Ідентифікатор автора.
        text: Текст коментаря.
        created_at: Дата створення коментаря.
    """

    id: int
    author_id: int
    text: str
    created_at: datetime


class PostIn(Schema):
    """Схема для створення або оновлення посту.

    Attributes:
        title: Заголовок посту.
        content: Текст посту.
        tag_ids: Список ідентифікаторів тегів.
    """

    title: str
    content: str
    tag_ids: List[int] = []


class PostOut(Schema):
    """Схема для відображення посту з тегами та коментарями.

    Attributes:
        id: Ідентифікатор посту.
        title: Заголовок посту.
        content: Текст посту.
        author_id: Ідентифікатор автора.
        tags: Список тегів.
        comments: Список коментарів.
        created_at: Дата створення посту.
        updated_at: Дата останнього оновлення посту.
    """

    id: int
    title: str
    content: str
    author_id: int
    tags: List[TagOut]
    comments: List[CommentOut]
    created_at: datetime
    updated_at: datetime