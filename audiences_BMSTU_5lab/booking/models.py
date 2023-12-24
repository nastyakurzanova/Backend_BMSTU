from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models, connection
from django.utils import timezone
from django.urls import reverse

class Audiences(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )
    name = models.CharField(max_length=1000, default="501", verbose_name="Номер")
    # number = models.CharField(max_length=1000, verbose_name="Номер")
    price = models.FloatField(default=5000.00, verbose_name="Цена")
    info = models.TextField(max_length=250, verbose_name="Информация", null=True)
    image = models.ImageField(verbose_name="Фото", null=False)
    corpus = models.TextField(max_length=20, verbose_name="Корпус")
    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"

    def get_absolute_url(self):
        return reverse("audiences_details", kwargs={"audiences_id": self.id})

    def get_delete_url(self):
        return reverse("audiences_delete", kwargs={"audiences_id": self.id})

    def delete(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE booking_audiences SET status = 2 WHERE id = %s", [self.pk])


# class Spare(models.Model):
#     STATUS_CHOICES = (
#         (1, 'Действует'),
#         (2, 'Удалена'),
#     )

#     name = models.CharField(max_length=100, default="Название авиазапчасти", verbose_name="Название")
#     status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="Статус")
#     image = models.ImageField(upload_to="spares", default="booking/default.jpg", verbose_name="Фото")
#     description = models.TextField(max_length=500, default='Описание авиазапчасти', verbose_name="Описание")
#     price = models.IntegerField(default=1000, verbose_name="Цена")
#     weight = models.FloatField(default=10.0, verbose_name="Вес")
#     rating = models.FloatField(default=4.5, verbose_name="Рейтинг")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Авиазапчасть"
#         verbose_name_plural = "Авиазапчасти"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Booking(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )
    # факт свободности аудитории в календаре
    FREE_AUDIENCES = (
        (0, 'Свободная'),
        (1, 'Занята')
    )
    audiences = models.ManyToManyField(Audiences, verbose_name="Аудитории", null=True)
    name = models.CharField(verbose_name="Номер", default="Номер аудитории")
    description = models.TextField(verbose_name="Описание", default="Описание аудитории", blank=True, null=True)
    free_audiences = models.IntegerField(verbose_name="Свободна ли аудитория", choices=FREE_AUDIENCES, blank=True, null=True)
    # audincess = models.ManyToManyField(Audiences, through='BookingAudiences')
    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    # date = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Покупатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Администратор", related_name='moderator', blank=True, null=True)

    date_created = models.DateTimeField(verbose_name="Дата создания", default=timezone.now())
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Покупатель", null=True)

    # owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    # moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return "Заявка №" + str(self.pk)

    class Meta:
        verbose_name = "Заявка бронирования"
        verbose_name_plural = "Заявки бронирования"
        ordering = ('-date_of_formation', )
        managed=True


class BookingAudiences(models.Model):
    audience = models.ForeignKey(Audiences, models.DO_NOTHING)
    booking = models.ForeignKey(Booking, models.DO_NOTHING)
    time_booking = models.DateTimeField(verbose_name="Время бронирования", blank=True, null=True)

    def __str__(self):
        return "Аудитория-Бронирование №" + str(self.pk)

    class Meta:
        managed=True # позволяет создавать и изменять таблицы
        verbose_name = "Аудитория-Бронирование"
        verbose_name_plural = "Аудитории-Бронирование"

# class Order(models.Model):
#     STATUS_CHOICES = (
#         (1, 'Введён'),
#         (2, 'В работе'),
#         (3, 'Завершён'),
#         (4, 'Отменён'),
#         (5, 'Удалён'),
#     )

#     status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="Статус", db_index=True)
#     date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
#     date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
#     date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)
    
#     owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Покупатель", related_name='owner', null=True)
#     moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Администратор", related_name='moderator', blank=True, null=True)

#     spares = models.ManyToManyField(Spare, verbose_name="Авиазапчасти", null=False)

#     delivery_date = models.IntegerField(default=-1, verbose_name="Дата доставки")

#     def __str__(self):
#         return "Заказ №" + str(self.pk)

#     class Meta:
#         verbose_name = "Заказ"
#         verbose_name_plural = "Заказы"
#         ordering = ('-date_of_formation', )
