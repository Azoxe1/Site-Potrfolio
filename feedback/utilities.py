from venv import logger
from django.core.mail import send_mail, BadHeaderError
from datetime import datetime, timedelta, date
from .models import Contact
from portfolio.settings import DEFAULT_FROM_EMAIL


def feedback_email_send(request, form):  # да, этот код надо переписать, согласен
    body = {
        'name': form.cleaned_data['name'],
        'telegram': form.cleaned_data['telegram'],
        'phone_number': str(form.cleaned_data['phone_number']),
        'selected_time': str(form.cleaned_data['selected_date']),
        'request_time': str(datetime.now()),
        'course_choose': 'Консультация с карьерным помощником.',
    }

    subject = f"Новое обращение №{Contact.objects.all().last().id}"
    message = (f"Имя: {body.get('name')}\n"
               f"Telegram: {body.get('telegram')}\n"
               f"Номер телефона: {body.get('phone_number')}\n\n"
               f"Желаемая дата: {str((Contact.objects.all().last().selected_date) + timedelta(hours=3))[:16]}\n"
               f"Дата создания заявки: {str(body.get('request_time'))[:16]}\n\n"
               f"Тема обращения: {body.get('course_choose')}\n"
               )
    try:
        send_mail(subject=subject,
                  message=message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=[DEFAULT_FROM_EMAIL])
    except BadHeaderError:
        logger.exception("Найден неккоректный заголовок")
