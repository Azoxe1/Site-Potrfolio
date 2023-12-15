from django.db import models
from datetime import datetime, timezone

tz_string = datetime.now().astimezone().tzname()


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    timezone = models.CharField(max_length=32, default=tz_string)
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone_number = models.CharField(max_length=200, verbose_name='Номер телефона')
    telegram = models.CharField(max_length=100, default='TG не указан', verbose_name='Telegram')
    selected_date = models.DateField(default=None, verbose_name='Выбранная дата')
    request_time = models.DateTimeField(auto_now=True, verbose_name='Дата создания запроса')
    course_choose = models.CharField(max_length=200, default='Консультация',
                                     verbose_name='Тема обращения')

    class Meta:
        verbose_name_plural = 'Обращения'
        verbose_name = 'Обращение'
        ordering = ['request_time', 'selected_date']
