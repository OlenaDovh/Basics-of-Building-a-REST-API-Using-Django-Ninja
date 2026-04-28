from django.db import models
from django.contrib.auth.models import User


class Server(models.Model):
    """Модель сервера для моніторингу.

    Attributes:
        name: Назва сервера.
        ip_address: IP-адреса сервера.
        status: Статус сервера (online/offline).
        owner: Власник сервера.
        created_at: Дата створення запису.
    """

    STATUS_CHOICES = [
        ('online', 'Увімкнений'),
        ('offline', 'Вимкнений'),
    ]

    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='online')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення сервера.

        Returns:
            Назва сервера.
        """
        return self.name


class Metric(models.Model):
    """Модель метрик сервера.

    Attributes:
        server: Сервер, до якого належать метрики.
        cpu: Завантаження CPU у відсотках.
        memory: Використання пам'яті у відсотках.
        load: Загальне навантаження системи.
        recorded_at: Час фіксації метрик.
    """

    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='metrics')
    cpu = models.FloatField()
    memory = models.FloatField()
    load = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення метрик.

        Returns:
            Рядок із назвою сервера та часом вимірювання.
        """
        return f"Метрики {self.server.name} о {self.recorded_at}"


class Alert(models.Model):
    """Модель системного сповіщення.

    Attributes:
        server: Сервер, до якого відноситься сповіщення.
        message: Текст сповіщення.
        created_at: Час створення сповіщення.
    """

    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення сповіщення.

        Returns:
            Рядок із назвою сервера.
        """
        return f"Сповіщення для {self.server.name}"