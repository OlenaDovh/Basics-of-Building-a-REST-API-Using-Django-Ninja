from ninja import Schema
from datetime import datetime


class ServerIn(Schema):
    """Схема для створення або оновлення сервера.

    Attributes:
        name: Назва сервера.
        ip_address: IP-адреса сервера.
        status: Статус сервера (online або offline).
    """

    name: str
    ip_address: str
    status: str = "online"


class ServerOut(Schema):
    """Схема відповіді для сервера.

    Attributes:
        id: Ідентифікатор сервера.
        name: Назва сервера.
        ip_address: IP-адреса сервера.
        status: Статус сервера.
        created_at: Дата створення запису.
    """

    id: int
    name: str
    ip_address: str
    status: str
    created_at: datetime


class ServerStatusIn(Schema):
    """Схема для оновлення статусу сервера.

    Attributes:
        status: Новий статус сервера (online або offline).
    """

    status: str


class MetricIn(Schema):
    """Схема для створення метрик сервера.

    Attributes:
        cpu: Завантаження CPU у відсотках.
        memory: Використання пам'яті у відсотках.
        load: Загальне навантаження системи.
    """

    cpu: float
    memory: float
    load: float


class MetricOut(Schema):
    """Схема відповіді для метрик сервера.

    Attributes:
        id: Ідентифікатор метрик.
        server_id: Ідентифікатор сервера.
        cpu: Завантаження CPU.
        memory: Використання пам'яті.
        load: Загальне навантаження.
        recorded_at: Час фіксації метрик.
    """

    id: int
    server_id: int
    cpu: float
    memory: float
    load: float
    recorded_at: datetime


class AlertOut(Schema):
    """Схема відповіді для сповіщення.

    Attributes:
        id: Ідентифікатор сповіщення.
        server_id: Ідентифікатор сервера.
        message: Текст сповіщення.
        created_at: Час створення сповіщення.
    """

    id: int
    server_id: int
    message: str
    created_at: datetime