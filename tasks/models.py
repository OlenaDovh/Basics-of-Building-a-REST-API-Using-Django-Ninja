from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Модель завдання.

    Attributes:
        title: Назва завдання.
        description: Опис завдання.
        status: Статус завдання (pending або done).
        due_date: Дата дедлайну виконання.
        created_at: Дата створення завдання.
        owner: Користувач-власник завдання.
    """

    STATUS_CHOICES = [
        ('pending', 'Не виконано'),
        ('done', 'Виконано'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self) -> str:
        """Повертає назву завдання.

        Returns:
            Назва завдання.
        """
        return self.title