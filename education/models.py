from typing import Optional

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """Модель студента.

    Представляє профіль студента, пов'язаний із користувачем системи.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Повертає рядкове представлення студента.

        Returns:
            Ім'я користувача, пов'язаного зі студентом.
        """
        return self.user.username


class Course(models.Model):
    """Модель курсу.

    Представляє навчальний курс, на який можуть записуватися студенти.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_grade(self) -> Optional[float]:
        """Обчислює середню оцінку для курсу.

        Returns:
            Середня оцінка студентів, округлена до 2 знаків,
            або None, якщо оцінок немає.
        """
        grades = self.enrollments.exclude(grade=None)
        if grades.exists():
            return round(sum(e.grade for e in grades) / grades.count(), 2)
        return None

    def __str__(self) -> str:
        """Повертає рядкове представлення курсу.

        Returns:
            Назва курсу.
        """
        return self.title


class Enrollment(models.Model):
    """Модель запису на курс.

    Представляє факт реєстрації студента на курс разом із оцінкою.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    grade = models.FloatField(null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self) -> str:
        """Повертає рядкове представлення запису.

        Returns:
            Рядок у форматі "студент — курс".
        """
        return f"{self.student} — {self.course}"