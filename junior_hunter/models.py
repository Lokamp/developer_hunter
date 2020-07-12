from django.db import models
from django.contrib.auth.models import User


class Specialty(models.Model):
    title = models.CharField(
        max_length=120
    )
    code = models.CharField(
        max_length=10,
    )
    picture = models.ImageField(
        upload_to='MEDIA_SPECIALITY_IMAGE_DIR'
    )

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Имя'
    )
    location = models.CharField(
        max_length=50,
        verbose_name='Город'
    )
    logo = models.ImageField(
        upload_to='MEDIA_COMPANY_IMAGE_DIR',
        verbose_name='Логотип'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    employee_count = models.IntegerField(
        verbose_name='Количество сотрудников'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="company"
    )

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(
        max_length=120,
        verbose_name='Название вакансии'
    )
    speciality = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name='Специальность'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name='Компания'
    )
    skills = models.TextField(
        verbose_name='Навыки'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    salary_min = models.IntegerField(
        verbose_name='Зарплата от'
    )
    salary_max = models.IntegerField(
        verbose_name='Зарплата до'
    )
    published_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(
        max_length=20
    )
    written_phone = models.CharField(
        max_length=20
    )
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )


class Resume(models.Model):
    class ResumeStatusChoices(models.TextChoices):
        LOOKING_WORK = 'LW', 'Ищу работу'
        NOT_LOOKING_WORK = 'NW', 'Не ищу работу'
        MAYBE_CONSIDER = 'MC', 'Рассматриваю предложения'

    class ResumeGradeChoices(models.TextChoices):
        INTERN = 'NB', 'Стажер'
        JUNIOR = 'JR', 'Джуниор'
        MIDDLE = 'ML', 'Миддл'
        SENIOR = 'SR', 'Синьор'
        LEAD = 'LD', 'Лид'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resume'
    )
    first_name = models.CharField(
        max_length=40,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=40,
        verbose_name='Фамилия'
    )
    status = models.CharField(
        max_length=2,
        choices=ResumeStatusChoices.choices,
        default=ResumeStatusChoices.NOT_LOOKING_WORK,
        verbose_name='Готовность к работе'
    )
    salary = models.IntegerField(
        verbose_name='Ожидаемое вознаграждение'
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name='resume',
        verbose_name='Специальность'
    )
    grade = models.CharField(
        max_length=2,
        choices=ResumeGradeChoices.choices,
        default=ResumeGradeChoices.INTERN,
        verbose_name='Квалификация'
    )
    education = models.TextField(
        verbose_name='Образование'
    )
    experience = models.TextField(
        verbose_name='Опыт работы'
    )
    portfolio = models.CharField(
        max_length=100,
        verbose_name='Портфолио'
    )
