from typing import Optional, Any
from datetime import datetime, date

from ninja import Schema


class StudentIn(Schema):
    """Схема для створення або оновлення студента.

    Attributes:
        username: Ім'я користувача, з яким пов'язується студент.
        phone: Номер телефону студента.
        birth_date: Дата народження студента.
    """

    username: str
    phone: str = ""
    birth_date: Optional[date] = None


class StudentOut(Schema):
    """Схема відповіді для студента.

    Attributes:
        id: Ідентифікатор студента.
        user_id: Ідентифікатор пов'язаного користувача.
        first_name: Ім'я користувача.
        last_name: Прізвище користувача.
        phone: Номер телефону.
        birth_date: Дата народження.
        created_at: Дата створення запису.
    """

    id: int
    user_id: int
    first_name: str
    last_name: str
    phone: str
    birth_date: Optional[date]
    created_at: datetime

    @staticmethod
    def resolve_first_name(obj: Any) -> str:
        """Отримує ім'я користувача зі зв'язаного об'єкта.

        Args:
            obj: Об'єкт студента.

        Returns:
            Ім'я користувача.
        """
        return obj.user.first_name

    @staticmethod
    def resolve_last_name(obj: Any) -> str:
        """Отримує прізвище користувача зі зв'язаного об'єкта.

        Args:
            obj: Об'єкт студента.

        Returns:
            Прізвище користувача.
        """
        return obj.user.last_name


class CourseIn(Schema):
    """Схема для створення або оновлення курсу.

    Attributes:
        title: Назва курсу.
        description: Опис курсу.
    """

    title: str
    description: str = ""


class CourseOut(Schema):
    """Схема відповіді для курсу.

    Attributes:
        id: Ідентифікатор курсу.
        title: Назва курсу.
        description: Опис курсу.
        average_grade: Середня оцінка студентів.
        created_at: Дата створення курсу.
    """

    id: int
    title: str
    description: str
    average_grade: Optional[float]
    created_at: datetime


class EnrollmentOut(Schema):
    """Схема відповіді для запису на курс.

    Attributes:
        id: Ідентифікатор запису.
        student_id: Ідентифікатор студента.
        course_id: Ідентифікатор курсу.
        grade: Оцінка студента.
        enrolled_at: Дата запису на курс.
    """

    id: int
    student_id: int
    course_id: int
    grade: Optional[float]
    enrolled_at: datetime


class GradeIn(Schema):
    """Схема для встановлення оцінки.

    Attributes:
        grade: Оцінка студента.
    """

    grade: float