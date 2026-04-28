from typing import Optional

from ninja.security import HttpBearer
from django.contrib.auth.models import User


class AuthBearer(HttpBearer):
    """Кастомна схема автентифікації через Bearer-токен.

    Використовує значення токена як username для пошуку користувача.
    """

    def authenticate(self, request, token: str) -> Optional[User]:
        """Аутентифікує користувача за токеном.

        Args:
            request: HTTP-запит.
            token: Bearer-токен (username користувача).

        Returns:
            Об'єкт користувача, якщо знайдено, інакше None.
        """
        try:
            user = User.objects.get(username=token)
            request.user = user
            return user
        except User.DoesNotExist:
            return None