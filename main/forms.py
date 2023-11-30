from django import forms
from .models import Contact
import datetime
from django.utils.timezone import now

class ContactForm(forms.ModelForm):
    selected_date = forms.DateField(

        initial=format(datetime.date.today(), '%Y-%m-%d'),
        label="Дата обратной связи",
        localize=True,
        widget=forms.widgets.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date',
                   'placeholder': 'Ваше имя',
                   'min': now().strftime('%Y-%m-%d'),
                   })
    )

    name = forms.CharField(
        min_length=2,
        label="Имя",
        widget=forms.TextInput(
            attrs={'placeholder': 'Ваше имя *'}
        )
    )

    phone_number = forms.IntegerField(
        label="Номер телефона",
        widget=forms.TextInput(
            attrs={'placeholder': 'Контактный телефон *'}
        )
    )
    telegram = forms.CharField(
        label="Ник в Telegram",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Ник в Telegram (необяз.)'}
        )
    )
    class Meta:
        model = Contact
        fields = ["id", "name", "phone_number", "telegram", "selected_date"]
