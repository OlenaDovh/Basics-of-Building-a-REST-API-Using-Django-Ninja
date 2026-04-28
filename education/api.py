from typing import Any, Dict, List

from django.contrib.auth.models import User
from ninja import NinjaAPI
from ninja.errors import HttpError

from .models import Student, Course, Enrollment
from .schemas import StudentIn, StudentOut, CourseIn, CourseOut, EnrollmentOut, GradeIn
from tasks.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer(), urls_namespace="education")


@api.post("/students", response=StudentOut)
def create_student(request: Any, payload: StudentIn) -> Student:
    """Створює новий профіль студента.

    Args:
        request: HTTP-запит користувача.
        payload: Дані для створення студента.

    Returns:
        Створений об'єкт студента.

    Raises:
        HttpError: Якщо користувача не знайдено або профіль студента вже існує.
    """
    data = payload.dict()
    username = data.pop("username")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise HttpError(404, f"Користувача '{username}' не знайдено")

    if Student.objects.filter(user=user).exists():
        raise HttpError(400, f"Профіль студента для '{username}' вже існує")

    student = Student.objects.create(user=user, **data)
    return student


@api.get("/students", response=List[StudentOut])
def list_students(request: Any) -> List[Student]:
    """Повертає список усіх студентів.

    Args:
        request: HTTP-запит користувача.

    Returns:
        Список об'єктів студентів.
    """
    return list(Student.objects.all())


@api.get("/students/{student_id}", response=StudentOut)
def get_student(request: Any, student_id: int) -> Student:
    """Повертає студента за ідентифікатором.

    Args:
        request: HTTP-запит користувача.
        student_id: Ідентифікатор студента.

    Returns:
        Об'єкт студента.

    Raises:
        HttpError: Якщо студента не знайдено.
    """
    try:
        return Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise HttpError(404, "Студента не знайдено")


@api.put("/students/{student_id}", response=StudentOut)
def update_student(request: Any, student_id: int, payload: StudentIn) -> Student:
    """Оновлює дані студента.

    Args:
        request: HTTP-запит користувача.
        student_id: Ідентифікатор студента.
        payload: Нові дані студента.

    Returns:
        Оновлений об'єкт студента.

    Raises:
        HttpError: Якщо студента або користувача не знайдено.
    """
    data = payload.dict()
    username = data.pop("username")

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise HttpError(404, "Студента не знайдено")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise HttpError(404, f"Користувача '{username}' не знайдено")

    student.user = user
    for attr, value in data.items():
        setattr(student, attr, value)
    student.save()
    return student


@api.delete("/students/{student_id}")
def delete_student(request: Any, student_id: int) -> Dict[str, bool]:
    """Видаляє студента за ідентифікатором.

    Args:
        request: HTTP-запит користувача.
        student_id: Ідентифікатор студента.

    Returns:
        Словник зі статусом успішного видалення.

    Raises:
        HttpError: Якщо студента не знайдено.
    """
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise HttpError(404, "Студента не знайдено")
    student.delete()
    return {"success": True}


@api.post("/courses", response=CourseOut)
def create_course(request: Any, payload: CourseIn) -> Course:
    """Створює новий курс.

    Args:
        request: HTTP-запит користувача.
        payload: Дані для створення курсу.

    Returns:
        Створений об'єкт курсу.
    """
    course = Course.objects.create(**payload.dict())
    return course


@api.get("/courses", response=List[CourseOut])
def list_courses(request: Any) -> List[Course]:
    """Повертає список усіх курсів.

    Args:
        request: HTTP-запит користувача.

    Returns:
        Список об'єктів курсів.
    """
    return list(Course.objects.all())


@api.get("/courses/{course_id}", response=CourseOut)
def get_course(request: Any, course_id: int) -> Course:
    """Повертає курс за ідентифікатором.

    Args:
        request: HTTP-запит користувача.
        course_id: Ідентифікатор курсу.

    Returns:
        Об'єкт курсу.

    Raises:
        HttpError: Якщо курс не знайдено.
    """
    try:
        return Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Курс не знайдено")


@api.put("/courses/{course_id}", response=CourseOut)
def update_course(request: Any, course_id: int, payload: CourseIn) -> Course:
    """Оновлює дані курсу.

    Args:
        request: HTTP-запит користувача.
        course_id: Ідентифікатор курсу.
        payload: Нові дані курсу.

    Returns:
        Оновлений об'єкт курсу.

    Raises:
        HttpError: Якщо курс не знайдено.
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Курс не знайдено")
    for attr, value in payload.dict().items():
        setattr(course, attr, value)
    course.save()
    return course


@api.delete("/courses/{course_id}")
def delete_course(request: Any, course_id: int) -> Dict[str, bool]:
    """Видаляє курс за ідентифікатором.

    Args:
        request: HTTP-запит користувача.
        course_id: Ідентифікатор курсу.

    Returns:
        Словник зі статусом успішного видалення.

    Raises:
        HttpError: Якщо курс не знайдено.
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Курс не знайдено")
    course.delete()
    return {"success": True}


@api.post("/courses/{course_id}/enroll", response=EnrollmentOut)
def enroll_student(request: Any, course_id: int, student_id: int) -> Enrollment:
    """Реєструє студента на курс.

    Args:
        request: HTTP-запит користувача.
        course_id: Ідентифікатор курсу.
        student_id: Ідентифікатор студента.

    Returns:
        Створений запис про реєстрацію.

    Raises:
        HttpError: Якщо студента або курс не знайдено, або студент уже зареєстрований.
    """
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise HttpError(404, "Студента не знайдено")
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Курс не знайдено")
    if Enrollment.objects.filter(student=student, course=course).exists():
        raise HttpError(400, "Студент вже зареєстрований на цей курс")
    enrollment = Enrollment.objects.create(student=student, course=course)
    return enrollment


@api.get("/courses/{course_id}/enrollments", response=List[EnrollmentOut])
def list_enrollments(request: Any, course_id: int) -> List[Enrollment]:
    """Повертає список реєстрацій на курс.

    Args:
        request: HTTP-запит користувача.
        course_id: Ідентифікатор курсу.

    Returns:
        Список записів про реєстрацію на курс.

    Raises:
        HttpError: Якщо курс не знайдено.
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Курс не знайдено")
    return list(course.enrollments.all())


@api.patch("/enrollments/{enrollment_id}/grade", response=EnrollmentOut)
def set_grade(request: Any, enrollment_id: int, payload: GradeIn) -> Enrollment:
    """Встановлює оцінку для запису про реєстрацію.

    Args:
        request: HTTP-запит користувача.
        enrollment_id: Ідентифікатор запису про реєстрацію.
        payload: Дані з оцінкою студента.

    Returns:
        Оновлений запис про реєстрацію.

    Raises:
        HttpError: Якщо оцінка поза допустимим діапазоном або запис не знайдено.
    """
    if not (0.0 <= payload.grade <= 100.0):
        raise HttpError(400, "Оцінка повинна бути від 0 до 100")
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        raise HttpError(404, "Запис не знайдено")
    enrollment.grade = payload.grade
    enrollment.save()
    return enrollment


@api.get("/courses/{course_id}/average", response=dict)
def course_average(request: Any, course_id: int) -> Dict[str, Any]:
    """Повертає середню оцінку для курсу.

    Args:
        request: HTTP-запит користувача.
        course_id: Ідентифікатор курсу.

    Returns:
        Словник із назвою курсу та середньою оцінкою.

    Raises:
        HttpError: Якщо курс не знайдено.
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Курс не знайдено")
    return {"course": course.title, "average_grade": course.average_grade()}