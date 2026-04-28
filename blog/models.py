from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Модель тегу для постів.

    Attributes:
        name: Назва тегу (унікальна).
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        """Повертає назву тегу.

        Returns:
            Назва тегу.
        """
        return self.name


class Post(models.Model):
    """Модель посту в блозі.

    Attributes:
        title: Заголовок посту.
        content: Текст посту.
        author: Користувач-автор посту.
        tags: Теги, пов’язані з постом.
        created_at: Дата створення посту.
        updated_at: Дата останнього оновлення посту.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Повертає заголовок посту.

        Returns:
            Заголовок посту.
        """
        return self.title


class Comment(models.Model):
    """Модель коментаря до посту.

    Attributes:
        post: Пост, до якого належить коментар.
        author: Користувач, який залишив коментар.
        text: Текст коментаря.
        created_at: Дата створення коментаря.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення коментаря.

        Returns:
            Рядок у форматі "Коментар від <username> до <post title>".
        """
        return f"Коментар від {self.author.username} до {self.post.title}"